from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.database import get_db
from app.models.users import User

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # get raw password from SecretStr
    password = request.password.get_secret_value()

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(user_id=user.id, role=user.role)
    refresh_token = create_refresh_token(user_id=user.id)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
