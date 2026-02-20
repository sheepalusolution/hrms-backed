from pydantic import BaseModel
from app.module.payroll.models import CurrencyEnum


class PayrollBase(BaseModel):
    salary: float
    month: int
    year: int
    currency: CurrencyEnum

class PayrollGenerateRequest(BaseModel):
    employee_id: int
    salary: float
    month: int
    year: int
    currency: CurrencyEnum# Admin will send this


class PayrollResponse(PayrollBase):
    id: int
    employee_id: int

    class Config:
        from_attributes = True