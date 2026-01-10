from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class LeaveManage(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    max_days_per_year = Column(Integer)
    status = Column(String(40))
    approved_by = Column(Integer, ForeignKey("users.id"))
    reason = Column(Text)

    employee = relationship("Employee", back_populates="leaves")
    approver = relationship("User", back_populates="approvals")
