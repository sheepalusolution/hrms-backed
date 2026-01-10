from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Designation(Base):
    __tablename__ = "designations"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    grade = Column(String(50))
    level = Column(String(50))
    dep_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="designations")
    employees = relationship("Employee", back_populates="designation")
