from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from sqlalchemy import Column, Integer, String, Text
class Role(Base):
    __tablename__ = "roles"

    id = Column (Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    users = relationship("User", back_populates="role")