from pydantic import BaseModel
from enum import Enum

# Optional: Currency Enum for Pydantic validation
class CurrencyEnum(str, Enum):
    NPR = "NPR"
    USD = "USD"
    EUR = "EUR"

class PayrollCreate(BaseModel):
    employee_id: int
    salary: float
    month: int              # 1-12
    year: int
    currency: CurrencyEnum  # NPR, USD, EUR

class PayrollOut(BaseModel):
    id: int
    employee_id: int
    salary: float
    month: int
    year: int
    currency: CurrencyEnum

    class Config:
        from_attribute = True
