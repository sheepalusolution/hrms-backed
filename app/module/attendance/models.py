
from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    attendance_date = Column(Date)

    clock_in = Column(TIMESTAMP(timezone=True))
    clock_out = Column(TIMESTAMP(timezone=True))

    working_hours = Column(Float, nullable=True)

    half_day = Column(Boolean)
    holiday = Column(Boolean)

    employee = relationship("Employee", back_populates="attendance")
