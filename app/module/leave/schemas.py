from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum


class LeaveStatus(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"


class LeaveDayType(str, Enum):
    Full = "Full"
    Half = "Half"


# 🔹 Apply leave
class LeaveCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str      
    day_type: LeaveDayType = LeaveDayType.Full  # Default to Full Day


# 🔹 Approve / Reject leave
class LeaveAction(BaseModel):
    status: LeaveStatus


# 🔹 Response
class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    approved_by: Optional[int]
    reason: Optional[str]
    day_type: LeaveDayType
    status: LeaveStatus

    model_config = ConfigDict(from_attributes=True)
