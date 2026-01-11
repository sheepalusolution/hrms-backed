from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Designation(Base):
    __tablename__ = "designation"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    grade = Column(String)
    level = Column(String)
    dep_id = Column(Integer, ForeignKey("department.id"))

    employees = relationship("Employee", back_populates="designation")
    department = relationship("Department", back_populates="designations")