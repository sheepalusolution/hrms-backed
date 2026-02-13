from sqlalchemy import Column, Integer, DateTime, Boolean, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))

    attendance_date = Column(DateTime(timezone=True), default=func.now())

    clock_in = Column(DateTime(timezone=True))
    clock_out = Column(DateTime(timezone=True))

    working_hours = Column(Float, default=0.0)

    half_day = Column(Boolean, default=False)
    holiday = Column(Boolean, default=False)
    work_from_home = Column(Boolean, default=False)

    employee = relationship("Employee", back_populates="attendance")
