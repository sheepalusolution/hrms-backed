from sqlalchemy import Column, Integer, String, Date, Time, Enum
import enum
from app.core.database import Base

class AttendanceStatus(enum.Enum):
    Present = "Present"
    Absent = "Absent"
    Leave = "Leave"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    check_in = Column(Time, nullable=True)
    check_out = Column(Time, nullable=True)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.Present)
