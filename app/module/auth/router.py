from fastapi import APIRouter, Depends, HTTPException, status, Form, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.auth.models import User
from app.core.security import verify_password, get_password_hash
from app.core.token import create_tokens, verify_refresh_token
from app.core.audit_logger import log_auth_event # Ensure this matches your file name
from app.module.auth.dependencies import get_current_user

router = APIRouter(tags=["Auth"])

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
        log_auth_event(db, "REGISTER_FAILED", email, ip, description="Email already registered")
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
        log_auth_event(db, "REGISTER_ERROR", email, ip, description=str(e))
        raise HTTPException(status_code=500, detail="Database error during registration")
    
    return {"msg": "User created successfully", "email": email}

@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    ip = request.client.host
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        # REQUIREMENT: Failed login attempts logged
        log_auth_event(db, "LOGIN_FAILED", form_data.username, ip, description="Invalid credentials")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # REQUIREMENT: Successful login logged
    log_auth_event(db, "LOGIN_SUCCESS", user.id, ip, role=str(user.role_id))

    payload = {"sub": str(user.id), "role_id": user.role_id}
    return create_tokens(payload)

@router.post("/logout")
def logout(
    request: Request, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # REQUIREMENT: Logout logged
    log_auth_event(db, "LOGOUT", current_user.id, request.client.host, role=str(current_user.role_id))
    return {"msg": "Successfully logged out"}

@router.post("/refresh")
def refresh(
    request: Request,
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    # REQUIREMENT: Token refresh logged
    ip = request.client.host
    payload = verify_refresh_token(refresh_token)
    
    if not payload:
        log_auth_event(db, "REFRESH_FAILED", "UNKNOWN", ip, description="Invalid refresh token")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    log_auth_event(db, "TOKEN_REFRESH", user.id, ip, role=str(user.role_id))
    return create_tokens({"sub": str(user.id), "role_id": user.role_id})