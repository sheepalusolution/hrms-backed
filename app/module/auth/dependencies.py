from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.module.auth.models import User
from app.core.roles import Role

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).get(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def role_required(role: Role):
    def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
