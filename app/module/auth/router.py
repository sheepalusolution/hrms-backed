from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.auth.models import User
from app.module.auth.schemas import LoginRequest, TokenResponse
from app.core.security import verify_password
from app.core.token import create_access_token, create_refresh_token, decode_token
from app.core.roles import Role

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# -------------------------
# LOGIN
# -------------------------
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {"sub": str(user.id), "role": user.role.value}

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer"
    }

# -------------------------
# CURRENT USER
# -------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        if payload["type"] != "access":
            raise HTTPException(status_code=401)

        user = db.query(User).get(int(payload["sub"]))
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# -------------------------
# ROLE GUARD
# -------------------------
def role_required(role: Role):
    def wrapper(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper
