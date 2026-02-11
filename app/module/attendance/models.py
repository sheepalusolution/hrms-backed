from sqlalchemy import Column, Integer,Date, String, Enum, DateTime, Boolean, Interval, ForeignKey
import enum
from app.core.database import Base
from sqlalchemy.orm import relationship

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    attendance_date = Column(Date)

    clock_in = Column(DateTime)
    clock_out = Column(DateTime)

    working_hours = Column(Interval)

    half_day = Column(Boolean)
    holiday = Column(Boolean)
    work_from_home = Column(Boolean)

    employee = relationship("Employee", back_populates="attendance")
    
