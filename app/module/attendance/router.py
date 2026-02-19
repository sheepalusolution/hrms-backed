from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.attendance.models import Attendance
from app.module.employee.models import Employee
from app.module.auth.dependencies import get_current_employee   # 👈 ADD THIS
from app.module.auth.dependencies import get_superadmin
from app.module.auth.models import User

router = APIRouter(tags=["Attendance"])

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

@router.get("/all-attendance")
def get_all_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_superadmin),  # 🔥 SuperAdmin only
):
    records = db.query(Attendance).order_by(Attendance.attendance_date.desc()).all()

    return {
        "message": "All attendance records",
        "total": len(records),
        "data": records,
    }

@router.post("/clock-in", status_code=status.HTTP_201_CREATED)
def clock_in(
    current_employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    today = datetime.now(tz=NEPAL_TZ).date()

    existing = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == current_employee.id,
            Attendance.attendance_date == today,
        )
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Already clocked in today")

    clock_in_time = datetime.now(tz=NEPAL_TZ)

    attendance = Attendance(
        employee_id=current_employee.id,
        attendance_date=today,
        clock_in=clock_in_time,
       
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {
        "message": "Clock-in successful",
        "clock_in_time": attendance.clock_in,
    }

@router.post("/clock-out")
def clock_out(
    current_employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    today = datetime.now(tz=NEPAL_TZ).date()

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == current_employee.id,
            Attendance.attendance_date == today,
        )
        .first()
    )

    if not attendance:
        raise HTTPException(status_code=400, detail="You must clock-in first")

    if attendance.clock_out:
        raise HTTPException(status_code=400, detail="Already clocked out")

    clock_in = attendance.clock_in
    if clock_in.tzinfo is None:
        clock_in = clock_in.replace(tzinfo=NEPAL_TZ)

    clock_out_time = datetime.now(tz=NEPAL_TZ)

    attendance.clock_out = clock_out_time
    duration = (clock_out_time - clock_in).total_seconds()
    attendance.working_hours = round(duration / 3600, 2)

    db.commit()
    db.refresh(attendance)

    return {
        "message": "Clock-out successful",
        "clock_out_time": attendance.clock_out,
        "working_hours": attendance.working_hours,
    }
@router.get("/monthly")
def get_monthly_attendance(
    year: int,
    month: int,
    current_employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    records = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == current_employee.id,
            extract("year", Attendance.attendance_date) == year,
            extract("month", Attendance.attendance_date) == month,
        )
        .order_by(Attendance.attendance_date)
        .all()
    )

    return records

@router.get("/today-status")
def today_status(
    current_employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    today = datetime.now(tz=NEPAL_TZ).date()

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == current_employee.id,
            Attendance.attendance_date == today,
        )
        .first()
    )

    if not attendance:
        return {"status": "Absent"}

    if attendance.clock_out:
        return {"status": "Completed"}

    return {"status": "Clocked-in"}
