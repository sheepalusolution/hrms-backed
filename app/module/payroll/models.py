from sqlalchemy import Column, Integer, Numeric, Enum, ForeignKey
from app.core.database import Base
import enum
from sqlalchemy.orm import relationship
# Define allowed currencies
class CurrencyEnum(enum.Enum):
    NPR = "NPR"
    USD = "USD"
    EUR = "EUR"

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    salary = Column(Numeric(10, 2))
    month = Column(Integer)
    year = Column(Integer)
    currency = Column(Enum(CurrencyEnum), nullable=False, default=CurrencyEnum.NPR)

    employee = relationship("Employee", back_populates="payroll")
