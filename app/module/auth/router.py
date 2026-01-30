# app/module/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status, Request, Body, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.auth.models import User
from app.core.security import verify_password, get_password_hash
from app.core.token import create_tokens, verify_refresh_token
from app.core.audit_logger import log_auth_event
from app.module.auth.dependencies import get_current_user
from app.module.auth.schemas import LoginRequest
from app.module.auth.schemas import UserCreate
from app.module.role.models import Role

router = APIRouter(tags=["auth"])

# REGISTER
# app/module/auth/router.py

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    form_data: UserCreate, # Or a specific RegisterRequest schema
    db: Session = Depends(get_db)
):
    # Check if user exists
    if db.query(User).filter(User.email == form_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Determine Role: 
    # You can pass 'role_id' in the body, or default to 2 (Employee)
    new_user = User(
        email=form_data.email,
        password_hash=get_password_hash(form_data.password),
        is_active=True,
        role_id=getattr(form_data, 'role_id', 2) # Default to Employee if not provided
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created successfully", "role_id": new_user.role_id}

# LOGIN
@router.post("/login")
def login(
    request: Request,
    form_data: LoginRequest,  # Pydantic model
    db: Session = Depends(get_db)
):
    ip = request.client.host
    email = form_data.email
    password = form_data.password

    # Fetch user from database
    user = db.query(User).filter(User.email == email).first()

    # Invalid credentials
    if not user or not verify_password(password, user.password_hash):
        log_auth_event(db, "LOGIN_FAILED", None, ip, description=f"Failed attempt for: {email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Successful login log
    log_auth_event(db, "LOGIN_SUCCESS", user.id, ip, role=str(user.role_id))

    # Map role_id to role name
    ROLE_MAP = {
        2: "hr_admin",
        1: "user",
        4: "superadmin",
          # add all your role mappings here
    }
    role_name = ROLE_MAP.get(user.role_id, "user")  # default to "user"

    # Create JWT payload
    payload = {"sub": str(user.email), "role_id": user.role_id, "role_name": role_name}

    # Generate tokens
    tokens = create_tokens(payload)  # returns {"access_token": ..., "refresh_token": ...}

    # Return tokens + role name + email
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "role_name": role_name,  # ✅ frontend can directly use this
        "email": user.email
    }

# PROFILE
@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role_id": current_user.role_id
    }

# REFRESH TOKEN
@router.post("/refresh")
def refresh(refresh_token: str = Body(...), db: Session = Depends(get_db)):
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_email = payload.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return create_tokens({"sub": user.email, "role_id": user.role_id})

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), request: Request = None, db: Session = Depends(get_db)):
    """
    Logs out the current user by recording a logout event.
    """
    ip = request.client.host if request else "unknown"
    log_auth_event(db, "LOGOUT", current_user.id, ip, role=str(current_user.role_id))
    return {"msg": "Successfully logged out"}