from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.database import get_db
from app.models.users import User
from app.core.dependencies import get_current_user
from app.core.roles import Roles, role_required

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = create_access_token(user_id=user.id, role=user.role)
    refresh_token = create_refresh_token(user_id=user.id)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token(request: RefreshRequest):
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        access_token = create_access_token(user_id=user_id, role=payload.get("role", "user"))
        refresh_token = create_refresh_token(user_id=user_id)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.get("/profile")
def profile(user=Depends(get_current_user)):
    return {"message": f"Hello User {user['user_id']}", "role": user["role"]}

@router.get("/admin-only")
def admin_route(user=Depends(role_required(Roles.ADMIN))):
    return {"message": f"Hello Admin {user['user_id']}"}
