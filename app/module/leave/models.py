import enum
from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

# Leave Status
class LeaveStatus(enum.Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

# Leave Type
class LeaveDayType(enum.Enum):
    Full = "Full"
    Half = "Half"

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    reason = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

 
    day_type = Column(Enum(LeaveDayType), default=LeaveDayType.Full)  # Full Day / Half Day
    status = Column(Enum(LeaveStatus), default=LeaveStatus.Pending)

    employee = relationship("Employee", back_populates="leaves")
    approved_by_user = relationship("User", back_populates="approved_leaves")
