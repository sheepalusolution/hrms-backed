from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

# =====================================================
# BASE SCHEMA
# =====================================================

class AttendanceBase(BaseModel):
    employee_id: int
    attendance_date: date
    half_day: bool = False
    holiday: bool = False
   


# =====================================================
# CREATE / UPDATE
# =====================================================

class AttendanceCreate(AttendanceBase):
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None


class AttendanceUpdate(BaseModel):
    half_day: Optional[bool] = None
    holiday: Optional[bool] = None
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None


# =====================================================
# CLOCK IN / CLOCK OUT REQUESTS
# =====================================================

class ClockInRequest(BaseModel):
   pass


class ClockOutRequest(BaseModel):
   pass


# =====================================================
# MANUAL MARK REQUEST (ADMIN USE)
# =====================================================

class MarkAttendanceRequest(BaseModel):
    employee_id: int
    attendance_date: date
    half_day: bool = False
    holiday: bool = False
    

# =====================================================
# FULL RESPONSE
# =====================================================

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    attendance_date: date

    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    working_hours: Optional[float] = None

    half_day: bool
    holiday: bool

    model_config = {"from_attributes": True}


# =====================================================
# DAILY DASHBOARD RESPONSE
# =====================================================

class DailyAttendanceResponse(BaseModel):
    employee_id: int
    attendance_date: date
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    working_hours: Optional[float] = None

    model_config = {"from_attributes": True}


# =====================================================
# MONTHLY SUMMARY RESPONSE
# =====================================================

class MonthlyAttendanceSummary(BaseModel):
    employee_id: int
    month: int
    year: int
    total_present: int
    total_absent: int
    total_leave: int
    total_working_hours: float

    model_config = {"from_attributes": True}


# =====================================================
# LIST RESPONSE
# =====================================================

class AttendanceListResponse(BaseModel):
    records: List[AttendanceResponse]

    model_config = {"from_attributes": True}
