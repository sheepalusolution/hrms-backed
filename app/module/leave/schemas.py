from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum


class LeaveStatus(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"


# 🔹 Apply leave
class LeaveCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: str


# 🔹 Approve / Reject leave
class LeaveAction(BaseModel):
    status: LeaveStatus


# 🔹 Response
class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    approved_by: Optional[int]
    reason: Optional[str]
    status: LeaveStatus

    model_config = ConfigDict(from_attributes=True)
