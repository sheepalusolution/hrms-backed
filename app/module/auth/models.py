from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from app.module.role.models import Role
    from app.module.employee.models import Employee
    from app.module.leave.models import Leave

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Use string references to avoid circular imports
    role = relationship("Role", back_populates="users")
    employee = relationship("Employee", back_populates="users")
    approved_leaves = relationship("Leave", back_populates="approved_by_user")
