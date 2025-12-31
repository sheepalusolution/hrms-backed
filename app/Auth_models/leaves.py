from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.database import Base
from sqlalchemy.orm import relationship
class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    status = Column(String(40))  # e.g., Approved, Pending, Rejected
    reason = Column(Text)
    max_days_per_year = Column(Integer) 
    
    employee = relationship("Employee", back_populates="leaves")