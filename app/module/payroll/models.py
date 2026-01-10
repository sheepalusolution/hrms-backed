from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Payroll(Base):
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    salary = Column(Numeric)
    currency = Column(String(50))
    month = Column(Integer)
    year = Column(Integer)

    employee = relationship("Employee", back_populates="payrolls")
