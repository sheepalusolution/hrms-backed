from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base

if TYPE_CHECKING:
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")
    employee = relationship("Employee", back_populates="user")
    approved_leaves = relationship("Leave", back_populates="approved_by_user")

    # 🔐 One user can have multiple refresh tokens (multiple sessions)
    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )


# 🔄 REFRESH TOKEN MODEL (ROTATION + REUSE DETECTION)
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)

    # 🔗 Token belongs to a user
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # 🔒 HASHED refresh token (NEVER store plaintext)
    token_hash = Column(String(255), unique=True, index=True, nullable=False)

    # 🚫 If true → token is invalid forever
    is_revoked = Column(Boolean, default=False)

    # 🕒 Issued time (for audit / cleanup)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔁 Relationship back to user
    user = relationship("User", back_populates="refresh_tokens")
