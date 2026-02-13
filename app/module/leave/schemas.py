from enum import Enum
from typing import Optional

from pydantic import BaseModel


# Use the same enum as in your SQLAlchemy model
class LeaveStatus(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"


# Schema for creating a leave
class LeaveCreate(BaseModel):
    employee_id: int
    reason: str


# Schema for updating leave status
class LeaveUpdateStatus(BaseModel):
    status: LeaveStatus
    approved_by: int


# Schema for returning leave data
class LeaveOut(BaseModel):
    id: int
    employee_id: int
    approved_by: Optional[int] = None
    reason: str
    status: LeaveStatus

    class Config:
        from_attribute = True
