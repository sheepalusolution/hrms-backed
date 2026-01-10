from sqlalchemy.orm import Session
from app.module.auth.models import User
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(db: Session, email: str, password: str, role_id: int):
    user = User(
        email=email,
        password_hash=hash_password(password),
        role_id=role_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
