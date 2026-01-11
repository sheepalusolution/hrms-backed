from sqlalchemy import Column, Integer, Numeric, String, Enum
from app.core.database import Base
import enum

# Define allowed currencies
class CurrencyEnum(enum.Enum):
    NPR = "NPR"
    USD = "USD"
    EUR = "EUR"

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False)
    salary = Column(Numeric(12, 2), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    currency = Column(Enum(CurrencyEnum), nullable=False, default=CurrencyEnum.NPR)
