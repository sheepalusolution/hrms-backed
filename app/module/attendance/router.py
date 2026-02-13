from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.database import get_db
from app.module.attendance.models import Attendance, AttendanceStatus
from app.module.employee.models import Employee

router = APIRouter(tags=["Attendance"])

# Nepal timezone
NEPAL_TZ = ZoneInfo("Asia/Kathmandu")


# ===============================
# CLOCK IN
# ===============================
@router.post("/clock-in", status_code=status.HTTP_201_CREATED)
def clock_in(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    today = datetime.now(tz=NEPAL_TZ).date()

    # Prevent double clock-in
    existing = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already clocked in today")

    # Save clock-in as timezone-aware datetime
    clock_in_time = datetime.now(tz=NEPAL_TZ)

    attendance = Attendance(
        employee_id=employee_id,
        attendance_date=today,
        clock_in=clock_in_time,
        status=AttendanceStatus.Present
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {
        "message": "Clock-in successful",
        "clock_in_time": attendance.clock_in
    }


# ===============================
# CLOCK OUT
# ===============================
@router.post("/clock-out", status_code=status.HTTP_200_OK)
def clock_out(employee_id: int, db: Session = Depends(get_db)):

    today = datetime.now(tz=NEPAL_TZ).date()

    # Fetch today's attendance record
    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance:
        raise HTTPException(status_code=400, detail="You must clock-in first")

    if attendance.clock_out:
        raise HTTPException(status_code=400, detail="Already clocked out")

    # Ensure clock_in is timezone-aware
    clock_in = attendance.clock_in
    if clock_in.tzinfo is None:
        clock_in = clock_in.replace(tzinfo=NEPAL_TZ)

    # Set clock_out as timezone-aware
    clock_out = datetime.now(tz=NEPAL_TZ)
    attendance.clock_out = clock_out

    # Calculate working hours (decimal)
    duration_seconds = (clock_out - clock_in).total_seconds()
    attendance.working_hours = round(duration_seconds / 3600, 2)

    db.commit()
    db.refresh(attendance)

    return {
        "message": "Clock-out successful",
        "clock_out_time": attendance.clock_out,
        "working_hours": attendance.working_hours
    }
