from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
