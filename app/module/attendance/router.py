from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime

from app.core.database import get_db
from app.module.attendance.models import Attendance, AttendanceStatus
from app.module.employee.models import Employee

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

@router.post("/clock-in", status_code=status.HTTP_201_CREATED)
def clock_in(
    employee_id: int,
    db: Session = Depends(get_db)
):
    today = date.today()

    existing = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already clocked in")

    attendance = Attendance(
        employee_id=employee_id,
        attendance_date=today,
        clock_in=datetime.utcnow(),
        status=AttendanceStatus.Present
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {"msg": "Clock-in successful"}
@router.post("/clock-out")
def clock_out(
    employee_id: int,
    db: Session = Depends(get_db)
):
    today = date.today()

    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance or not attendance.clock_in:
        raise HTTPException(status_code=400, detail="Clock-in not found")

    attendance.clock_out = datetime.utcnow()
    attendance.working_hours = attendance.clock_out - attendance.clock_in

    db.commit()

    return {"msg": "Clock-out successful"}
@router.post("/mark")
def mark_attendance(
    employee_id: int,
    attendance_date: date,
    status: AttendanceStatus,
    half_day: bool = False,
    holiday: bool = False,
    wfh: bool = False,
    db: Session = Depends(get_db)
):
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
    return {"msg": "Attendance updated"}
@router.get("/employee/{employee_id}")
def get_employee_attendance(
    employee_id: int,
    db: Session = Depends(get_db)
):
    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).order_by(Attendance.attendance_date.desc()).all()

    return records
@router.get("/date/{attendance_date}")
def get_attendance_by_date(
    attendance_date: date,
    db: Session = Depends(get_db)
):
    records = db.query(Attendance).filter(
        Attendance.attendance_date == attendance_date
    ).all()

    return records
