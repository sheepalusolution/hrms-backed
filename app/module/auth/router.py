from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.token_blacklist import TokenBlacklist
from app.core.audit_logger import log_audit
from app.core.roles import Roles, role_required
from app.module.auth.models import User  # adjust path if different
from app.module.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db), request: Request = None):
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.verify_password(password):  # assumes User model has verify_password()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)

    # Log audit event
    ip = request.client.host if request else None
    log_audit(user.id, user.role, "login", ip_address=ip)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token(refresh_token: str):
    if TokenBlacklist.is_blacklisted(refresh_token):
        raise HTTPException(status_code=403, detail="Token has been revoked")

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_access_token = create_access_token(user_id, payload.get("role"))
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(refresh_token: str, current_user: User = Depends(get_current_user)):
    # Add refresh token to blacklist
    TokenBlacklist.add_token(refresh_token)

    log_audit(current_user.id, current_user.role, "logout")
    return {"detail": "Successfully logged out"}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "full_name": getattr(current_user, "full_name", None)
    }

@router.get("/admin-only")
def admin_only(user=Depends(role_required(Roles.ADMIN))):
    return {"message": f"Hello, {user.username}. You are an ADMIN!"}
