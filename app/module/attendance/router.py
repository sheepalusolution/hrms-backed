from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import  datetime
from zoneinfo import ZoneInfo

from app.core.database import get_db
from app.module.attendance.models import Attendance
from app.module.employee.models import Employee

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

# CLOCK IN

@router.post("/clock-in", status_code=status.HTTP_201_CREATED)
def clock_in(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    today = datetime.now(tz=NEPAL_TZ).date()  

    existing = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already clocked in today")

    attendance = Attendance(
        employee_id=employee_id,
        attendance_date=today,
        clock_in=datetime.now(tz=NEPAL_TZ),  
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {
        "message": "Clock-in successful",
        "clock_in_time": attendance.clock_in
    }

# CLOCK OUT

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



    db.commit()
    db.refresh(attendance)

    return {
        "message": "Clock-out successful",
        "clock_out_time": attendance.clock_out,
    }
