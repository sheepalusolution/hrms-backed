from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from app.module.auth.models import User
    from app.module.employee.models import Employee # Add this for type hinting

class Role(Base):
    __tablename__ = "roles" # This is the name used in ForeignKey("roles.id")

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Relationships
    # Ensure 'role' exists as a relationship in your User model
    users = relationship("User", back_populates="role") 
    
    # Ensure 'role' exists as a relationship in your Employee model
    employees = relationship("Employee", back_populates="role")