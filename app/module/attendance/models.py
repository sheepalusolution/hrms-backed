from sqlalchemy import Column, Integer,Date, String, Enum, DateTime, Boolean, Interval, ForeignKey
import enum
from app.core.database import Base
from sqlalchemy.orm import relationship
class AttendanceStatus(enum.Enum):
    Present = "Present"
    Absent = "Absent"
    Leave = "Leave"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    attendance_date = Column(Date)

    clock_in = Column(DateTime)
    clock_out = Column(DateTime)

    late_or_early_exit = Column(Boolean)
    working_hours = Column(Interval)

    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.Present)
    half_day = Column(Boolean)
    holiday = Column(Boolean)
    work_from_home = Column(Boolean)

    employee = relationship("Employee", back_populates="attendance")
    