from fastapi import APIRouter, Depends, HTTPException, status, Form, Request, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.auth.models import User
from app.core.security import verify_password, get_password_hash
from app.core.token import create_tokens, verify_refresh_token
from app.core.audit_logger import log_auth_event 
from app.module.auth.dependencies import get_current_user

router = APIRouter(tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# REGISTER
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    ip = request.client.host
    user_exists = db.query(User).filter(User.email == email).first()
    
    if user_exists:
        log_auth_event(db, "REGISTER_FAILED", None, ip, description=f"Duplicate email: {email}")
        raise HTTPException(status_code=400, detail="A user with this email already exists.")
    
    new_user = User(
        email=email,
        password_hash=get_password_hash(password),
        is_active=True,
        role_id=1 
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        log_auth_event(db, "REGISTER_SUCCESS", new_user.id, ip, role="1")
    except Exception as e:
        db.rollback()
        log_auth_event(db, "REGISTER_ERROR", None, ip, description=f"DB Error for {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error during registration")
    
    return {"msg": "User created successfully", "email": email}

# LOGIN
@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    ip = request.client.host
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        log_auth_event(db, "LOGIN_FAILED", None, ip, description=f"Failed attempt for: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    log_auth_event(db, "LOGIN_SUCCESS", user.id, ip, role=str(user.role_id))

    payload = {"sub": str(user.email), "role_id": user.role_id}  # sub=email is safer
    return create_tokens(payload)

# LOGOUT
@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    request: Request = None,
    db: Session = Depends(get_db)
):
    # Audit log
    log_auth_event(
        db=db, 
        action="LOGOUT_SUCCESS", 
        user_id=current_user.id, 
        ip=request.client.host if request else "N/A",
        role=str(current_user.role_id),
        description=f"User {current_user.email} logged out successfully"
    )
    return {"msg": "Successfully logged out"}

# PROFILE
@router.get("/profile")
def profile(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role_id": user.role_id
    }

# REFRESH
@router.post("/refresh")
def refresh(
    request: Request,
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    ip = request.client.host
    payload = verify_refresh_token(refresh_token)
    
    if not payload:
        log_auth_event(db, "REFRESH_FAILED", None, ip, description="Expired/Invalid refresh token")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_email = payload.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    log_auth_event(db, "TOKEN_REFRESH_SUCCESS", user.id, ip, role=str(user.role_id))
    
    return create_tokens({"sub": str(user.email), "role_id": user.role_id})
