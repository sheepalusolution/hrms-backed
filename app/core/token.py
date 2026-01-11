from datetime import timedelta
from app.core.security import create_access_token, create_refresh_token

def create_tokens(data: dict):
  
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
