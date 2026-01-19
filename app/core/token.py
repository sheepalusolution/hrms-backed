import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def create_tokens(data: dict):
    """Create access and refresh tokens"""
    
    # 1. Access Token (expires in 30 mins)
    access_token_expires = datetime.utcnow() + timedelta(minutes=30)
    access_payload = data.copy()
    access_payload.update({"exp": access_token_expires})
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

    # 2. Refresh Token (expires in 7 days)
    refresh_token_expires = datetime.utcnow() + timedelta(days=7)
    refresh_payload = data.copy()
    refresh_payload.update({"exp": refresh_token_expires})
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def verify_refresh_token(token: str) -> Optional[dict]:
    """Verify refresh token and return payload"""
    try:
        # Decodes and checks expiration (exp) automatically
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None