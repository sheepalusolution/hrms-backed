from sqlalchemy import Column, Integer, Date, Time, Boolean, ForeignKey, String, Interval
from sqlalchemy.orm import relationship
from app.core.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    attendance_date = Column(Date)
    clock_in = Column(Time)
    clock_out = Column(Time)
    late_exit = Column(Boolean, default=False)
    working_hours = Column(Interval)
    status = Column(String(50))  # Present, Absent, Late
    half_day = Column(Boolean, default=False)
    holiday = Column(Boolean, default=False)
    work_from_home = Column(Boolean, default=False)

    employee = relationship("Employee", back_populates="attendance")
