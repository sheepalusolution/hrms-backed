from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class AttendanceCreate(BaseModel):
    employee_id: int
    work_from_home: Optional[bool] = False
    half_day: Optional[bool] = False
    holiday: Optional[bool] = False

class AttendanceOut(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    clock_in: Optional[time]
    clock_out: Optional[time]
    status: str
    working_hours: Optional[str]
    work_from_home: bool
    half_day: bool
    holiday: bool

    class Config:
        orm_mode = True
