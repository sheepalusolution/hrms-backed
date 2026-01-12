from sqlalchemy import Column, Integer, String, Date, Enum
from app.core.database import Base
import enum
from sqlalchemy.orm import relationship
# Define an Enum class for allowed leave statuses
class LeaveStatus(enum.Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.Pending)
    
    employee = relationship("Employee", back_populates="leaves")
 