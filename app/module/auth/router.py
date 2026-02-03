# app/module/auth/router.py

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Body
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash
from app.core.token import create_tokens, generate_refresh_token, hash_refresh_token
from app.core.audit_logger import log_auth_event

from app.module.auth.models import User, RefreshToken
from app.module.auth.schemas import LoginRequest, UserCreate
from app.module.auth.dependencies import get_current_user

router = APIRouter(tags=["auth"])

# ------------------------
# REGISTER
# ------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    form_data: UserCreate,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.email == form_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=form_data.email,
        password_hash=get_password_hash(form_data.password),
        is_active=True,
        role_id=form_data.role_id  # default Employee
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "msg": "User created successfully",
        "role_id": new_user.role_id
    }


# ------------------------
# LOGIN
# ------------------------
@router.post("/login")
def login(
    request: Request,
    form_data: LoginRequest,
    db: Session = Depends(get_db)
):
    ip = request.client.host
    email = form_data.email
    password = form_data.password

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        log_auth_event(
            db,
            "LOGIN_FAILED",
            None,
            ip,
            description=f"Failed attempt for {email}"
        )
        raise HTTPException(status_code=401, detail="Invalid email or password")

    log_auth_event(
        db,
        "LOGIN_SUCCESS",
        user.id,
        ip,
        role=str(user.role_id)
    )

    ROLE_MAP = {
        1: "user",
        2: "hr_admin",
        4: "superadmin",
        7: "manager",
        8: "recruiter",
        6: "finance"
    }

    role_name = ROLE_MAP.get(user.role_id, "user")

    payload = {
        "sub": user.email,
        "role_id": user.role_id,
        "role_name": role_name
    }

    # Access token
    tokens = create_tokens(payload)

    # 🔐 Refresh token (ROTATION READY)
    raw_refresh_token = generate_refresh_token()
    refresh_token_hash = hash_refresh_token(raw_refresh_token)

    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=refresh_token_hash
        )
    )
    db.commit()

    tokens["refresh_token"] = raw_refresh_token

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "role_name": role_name,
        "email": user.email
    }


# ------------------------
# PROFILE
# ------------------------
@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role_id": current_user.role_id
    }


# ------------------------
# REFRESH TOKEN (ROTATION + REUSE DETECTION)
# ------------------------
@router.post("/refresh")
def refresh(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    token_hash = hash_refresh_token(refresh_token)

    token_db = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).first()

    # 🚨 Token reuse or invalid token
    if not token_db or token_db.is_revoked:
        if token_db:
            db.query(RefreshToken).filter(
                RefreshToken.user_id == token_db.user_id
            ).update({"is_revoked": True})
            db.commit()

        raise HTTPException(
            status_code=401,
            detail="Refresh token reuse detected. Session revoked."
        )

    user = db.query(User).filter(User.id == token_db.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 🔒 Invalidate old refresh token
    token_db.is_revoked = True

    # 🔄 Issue new refresh token
    new_refresh_raw = generate_refresh_token()
    new_refresh_hash = hash_refresh_token(new_refresh_raw)

    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=new_refresh_hash
        )
    )

    db.commit()

    tokens = create_tokens({
        "sub": user.email,
        "role_id": user.role_id
    })

    tokens["refresh_token"] = new_refresh_raw

    return tokens


# ------------------------
# LOGOUT (REVOKE ALL SESSIONS)
# ------------------------
@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    request: Request = None,
    db: Session = Depends(get_db)
):
    ip = request.client.host if request else "unknown"

    # 🔒 Revoke all refresh tokens for user
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id
    ).update({"is_revoked": True})

    db.commit()

    log_auth_event(
        db,
        "LOGOUT",
        current_user.id,
        ip,
        role=str(current_user.role_id)
    )

    return {"msg": "Successfully logged out"}
