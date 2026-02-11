from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from enum import Enum

class AttendanceStatusEnum(str, Enum):
    Present = "Present"
    Absent = "Absent"
    Leave = "Leave"

class ClockInRequest(BaseModel):
    employee_id: int

class ClockOutRequest(BaseModel):
    employee_id: int

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None


    model_config = {
        "from_attributes": True  
    }
