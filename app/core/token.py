import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

import jwt

from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


# =========================================================
# ACCESS TOKEN (JWT — short lived)
# =========================================================
def create_access_token(data: dict, expires_minutes: int = 30) -> str:
    """
    Creates a short-lived JWT access token.
    Used for authorization.
    """
    payload = data.copy()
    payload.update(
        {
            "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
            "type": "access",
        }
    )
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# =========================================================
# REFRESH TOKEN (OPAQUE — ROTATED)
# =========================================================
def generate_refresh_token() -> str:
    """
    Generates a cryptographically secure opaque refresh token.
    NOT a JWT.
    """
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    """
    Hashes refresh token before DB storage.
    Plaintext token is NEVER stored.
    """
    return hashlib.sha256(token.encode()).hexdigest()


# =========================================================
# TOKEN PAIR CREATION
# =========================================================
def create_tokens(data: dict) -> dict:
    """
    Creates ONLY the access token.
    Refresh token is generated & rotated separately.
    """
    return {"access_token": create_access_token(data), "token_type": "bearer"}


# =========================================================
# VERIFY ACCESS TOKEN ONLY
# =========================================================
def verify_access_token(token: str) -> Optional[dict]:
    """
    Verifies access token and returns payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None

        print(f"Token verified for user_id: {payload.get('user_id')}")
        return payload
    except jwt.PyJWTError:
        return None
