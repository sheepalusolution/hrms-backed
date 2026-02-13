from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Designation(Base):
    __tablename__ = "designation"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    grade = Column(String)
    level = Column(String)
    dep_id = Column(Integer, ForeignKey("department.id"))

    department = relationship("Department", back_populates="designations")
