from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    salary = Column(Numeric)
    currency = Column(String(10))
    month = Column(Integer)
    year = Column(Integer)

    employee = relationship("Employee", back_populates="payroll")