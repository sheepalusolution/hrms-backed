from sqlalchemy.orm import Session
from fastapi import HTTPException
import hashlib

from app.module.auth.models import User, RefreshToken
from app.core.token import (
    create_tokens,
    generate_refresh_token,
    hash_refresh_token
)

# ======================================================
# PASSWORD UTILITIES
# ======================================================
def hash_password(password: str) -> str:
    """
    Hash user password before storing.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# ======================================================
# USER CREATION
# ======================================================
def create_user(db: Session, email: str, password: str, role_id: int):
    """
    Create a new user.
    """
    user = User(
        email=email,
        password_hash=hash_password(password),
        role_id=role_id,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ======================================================
# REFRESH TOKEN ROTATION SERVICE
# ======================================================
def rotate_refresh_token(
    raw_refresh_token: str,
    db: Session
) -> dict:
    
    # 🔐 Hash incoming refresh token
    token_hash = hash_refresh_token(raw_refresh_token)

    token_db = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).first()

    # 🚨 Token reuse or invalid token
    if not token_db or token_db.is_revoked:
        if token_db:
            # Revoke all sessions for user
            db.query(RefreshToken).filter(
                RefreshToken.user_id == token_db.user_id
            ).update({"is_revoked": True})
            db.commit()

        raise HTTPException(
            status_code=401,
            detail="Refresh token reuse detected. Session revoked."
        )

    # Get user
    user = db.query(User).filter(
        User.id == token_db.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 🔒 Invalidate old refresh token
    token_db.is_revoked = True

    # 🔄 Generate new refresh token
    new_refresh_raw = generate_refresh_token()
    new_refresh_hash = hash_refresh_token(new_refresh_raw)

    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=new_refresh_hash
        )
    )

    db.commit()

    # 🔑 Create new access token
    tokens = create_tokens({
        "sub": user.email,
        "role_id": user.role_id
    })

    # Attach rotated refresh token
    tokens["refresh_token"] = new_refresh_raw

    return tokens
