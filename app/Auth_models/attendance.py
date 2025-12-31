from sqlalchemy import Column, Integer, Date, Time, Boolean, ForeignKey, String, Interval
from app.database import Base
from sqlalchemy.orm import relationship
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    clock_in = Column(Time)
    clock_out = Column(Time)
    status = Column(String(50), nullable=False)  # e.g., 'Present', 'Absent', 'Late'
    work_from_home = Column(Boolean, default=False)
    late_exit = Column(Boolean, default=False)  # True if employee left late/early exit
    working_hours = Column(Interval)  # Stores total working duration
    half_day = Column(Boolean, default=False)
    holiday = Column(Boolean, default=False)
    
    employee = relationship("Employee", back_populates="attendance")