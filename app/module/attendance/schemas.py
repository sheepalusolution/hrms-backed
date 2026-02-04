from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from enum import Enum
class AttendanceStatusEnum(str, Enum):
    Present = "Present"
    Absent = "Absent"
    Leave = "Leave"
class AttendanceBase(BaseModel):
    employee_id: int
    attendance_date: date
    status: AttendanceStatusEnum = AttendanceStatusEnum.Present
    half_day: Optional[bool] = False
    holiday: Optional[bool] = False
    work_from_home: Optional[bool] = False
class ClockInRequest(BaseModel):
    employee_id: int
class ClockOutRequest(BaseModel):
    employee_id: int
class MarkAttendanceRequest(BaseModel):
    employee_id: int
    attendance_date: date
    status: AttendanceStatusEnum
    half_day: Optional[bool] = False
    holiday: Optional[bool] = False
    work_from_home: Optional[bool] = False
class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    clock_in: Optional[datetime]
    clock_out: Optional[datetime]
    working_hours: Optional[str]

    status: AttendanceStatusEnum
    half_day: bool
    holiday: bool
    work_from_home: bool

    class Config:
        orm_mode = True
class DailyAttendanceResponse(BaseModel):
    employee_id: int
    attendance_date: date
    status: AttendanceStatusEnum
    clock_in: Optional[datetime]
    clock_out: Optional[datetime]

    class Config:
        orm_mode = True
