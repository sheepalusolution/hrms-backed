from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


# =====================================================
# ENUMS
# =====================================================

class AttendanceStatusEnum(str, Enum):
    Present = "Present"
    Absent = "Absent"
    Leave = "Leave"
    Late = "Late"
    Half_Day = "Half_Day"


# =====================================================
# BASE SCHEMA
# =====================================================

class AttendanceBase(BaseModel):
    employee_id: int
    attendance_date: date
    status: AttendanceStatusEnum = AttendanceStatusEnum.Present
    half_day: bool = False
    holiday: bool = False
    work_from_home: bool = False


# =====================================================
# CREATE / UPDATE
# =====================================================

class AttendanceCreate(AttendanceBase):
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None


class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatusEnum] = None
    half_day: Optional[bool] = None
    holiday: Optional[bool] = None
    work_from_home: Optional[bool] = None
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None


# =====================================================
# CLOCK IN / CLOCK OUT REQUESTS
# =====================================================

class ClockInRequest(BaseModel):
    employee_id: int


class ClockOutRequest(BaseModel):
    employee_id: int


# =====================================================
# MANUAL MARK REQUEST (ADMIN USE)
# =====================================================

class MarkAttendanceRequest(BaseModel):
    employee_id: int
    attendance_date: date
    status: AttendanceStatusEnum
    half_day: bool = False
    holiday: bool = False
    work_from_home: bool = False


# =====================================================
# FULL RESPONSE
# =====================================================

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date

    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    working_hours: Optional[float] = None  # stored as float hours

    status: AttendanceStatusEnum
    half_day: bool
    holiday: bool
    work_from_home: bool

    model_config = {
        "from_attributes": True
    }


# =====================================================
# DAILY DASHBOARD RESPONSE
# =====================================================

class DailyAttendanceResponse(BaseModel):
    employee_id: int
    attendance_date: date
    status: AttendanceStatusEnum
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    working_hours: Optional[float] = None

    model_config = {
        "from_attributes": True
    }


# =====================================================
# MONTHLY SUMMARY RESPONSE (PRO LEVEL)
# =====================================================

class MonthlyAttendanceSummary(BaseModel):
    employee_id: int
    month: int
    year: int
    total_present: int
    total_absent: int
    total_leave: int
    total_late: int
    total_working_hours: float

    model_config = {
        "from_attributes": True
    }


# =====================================================
# LIST RESPONSE
# =====================================================

class AttendanceListResponse(BaseModel):
    records: List[AttendanceResponse]

    model_config = {
        "from_attributes": True
    }
