from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
class Designation(Base):
    __tablename__ = "designations"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    grade = Column(String(50))
    level = Column(String(50))
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    employees = relationship("Employee", back_populates="designation")