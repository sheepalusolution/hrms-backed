import enum

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


# Define an Enum class for allowed leave statuses
class LeaveStatus(enum.Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    reason = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    status = Column(Enum(LeaveStatus), default=LeaveStatus.Pending)

    employee = relationship("Employee", back_populates="leaves")
    approved_by_user = relationship("User", back_populates="approved_leaves")
