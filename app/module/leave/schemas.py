from pydantic import BaseModel
from datetime import date

class LeaveCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: str | None = None
    status: str = "Pending"
    status: str = "Approved"
    status: str = "Rejected"

class LeaveOut(BaseModel):
    id: int
    employee_id: int
    start_date: date
    end_date: date
    reason: str | None
    status: str

    class Config:
        from_attribute = True
