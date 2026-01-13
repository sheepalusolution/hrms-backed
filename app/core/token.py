from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

ACCESS_EXPIRE = 15
REFRESH_EXPIRE = 7

def create_tokens(data: dict):
    access = data.copy()
    refresh = data.copy()

    access["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE)
    refresh["exp"] = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE)

    return {
        "access_token": jwt.encode(access, settings.SECRET_KEY, algorithm="HS256"),
        "refresh_token": jwt.encode(refresh, settings.SECRET_KEY, algorithm="HS256"),
        "token_type": "bearer"
    }
