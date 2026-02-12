
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.core.database import get_db
from app.module.attendance.models import Attendance
from app.module.employee.models import Employee

router = APIRouter(
    tags=["Attendance"]
)

# Set Nepal timezone
NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

# ===============================
# CLOCK IN
# ===============================
@router.post("/clock-in", status_code=status.HTTP_201_CREATED)
def clock_in(employee_id: int, db: Session = Depends(get_db)):

    # Check employee exists
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    today = datetime.now(tz=NEPAL_TZ).date()  # Actual date in Nepal timezone

    # Prevent double clock-in
    existing = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already clocked in today")

    attendance = Attendance(
        employee_id=employee_id,
        attendance_date=today,
        clock_in=datetime.now(tz=NEPAL_TZ),  # Actual time in Nepal timezone
       
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
@router.post("/clock-out")
def clock_out(employee_id: int, db: Session = Depends(get_db)):

    today = datetime.now(tz=NEPAL_TZ).date()

    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance:
        raise HTTPException(status_code=400, detail="You must clock-in first")

    if attendance.clock_out:
        raise HTTPException(status_code=400, detail="Already clocked out")

    attendance.clock_out = datetime.now(tz=NEPAL_TZ)

    # Calculate working time in hours (float)
    time_difference = attendance.clock_out - attendance.clock_in
    attendance.working_hours = round(time_difference.total_seconds() / 3600, 2)

    db.commit()
    db.refresh(attendance)

    return {
        "message": "Clock-out successful",
        "clock_out_time": attendance.clock_out,
        "working_hours": attendance.working_hours
    }


# ===============================
# MANUAL MARK (ADMIN USE)
# ===============================
@router.post("/mark")
def mark_attendance(
    employee_id: int,
    attendance_date: date,
    
    half_day: bool = False,
    holiday: bool = False,
    wfh: bool = False,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == attendance_date
    ).first()

    if attendance:
        attendance.status = status
        attendance.half_day = half_day
        attendance.holiday = holiday
        attendance.work_from_home = wfh
    else:
        attendance = Attendance(
            employee_id=employee_id,
            attendance_date=attendance_date,
            status=status,
            half_day=half_day,
            holiday=holiday,
            work_from_home=wfh
        )
        db.add(attendance)

    db.commit()
    db.refresh(attendance)

    return {"message": "Attendance updated successfully"}


# ===============================
# GET EMPLOYEE ATTENDANCE
# ===============================
@router.get("/employee/{employee_id}")
def get_employee_attendance(employee_id: int, db: Session = Depends(get_db)):

    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).order_by(Attendance.attendance_date.desc()).all()

    return records


# ===============================
# GET BY DATE
# ===============================
@router.get("/date/{attendance_date}")
def get_attendance_by_date(attendance_date: date, db: Session = Depends(get_db)):

    records = db.query(Attendance).filter(
        Attendance.attendance_date == attendance_date
    ).all()

    return records
