from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.module.attendance.models import Attendance
from app.module.employee.models import Employee
from app.module.attendance.schemas import AttendanceCreate, AttendanceOut

router = APIRouter()

# Clock-in endpoint
@router.post("/attendance/clock-in", response_model=AttendanceOut)
def clock_in(attendance_data: AttendanceCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == attendance_data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    today = date.today()
    existing = db.query(Attendance).filter(
        Attendance.employee_id == employee.id,
        Attendance.attendance_date == today
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for today")

    attendance = Attendance(
        employee_id=employee.id,
        attendance_date=today,
        clock_in=datetime.now().time(),
        status="Present",
        work_from_home=attendance_data.work_from_home,
        half_day=attendance_data.half_day,
        holiday=attendance_data.holiday
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

# Clock-out endpoint
@router.post("/attendance/clock-out", response_model=AttendanceOut)
def clock_out(employee_id: int, db: Session = Depends(get_db)):
    today = date.today()
    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.attendance_date == today
    ).first()

    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")

    if attendance.clock_out:
        raise HTTPException(status_code=400, detail="Already clocked out today")

    attendance.clock_out = datetime.now().time()

    # Calculate working hours
    if attendance.clock_in:
        start = datetime.combine(today, attendance.clock_in)
        end = datetime.combine(today, attendance.clock_out)
        attendance.working_hours = end - start

    db.commit()
    db.refresh(attendance)
    return attendance

# Get attendance records
@router.get("/attendance/{employee_id}", response_model=list[AttendanceOut])
def get_attendance(employee_id: int, month: int = None, db: Session = Depends(get_db)):
    query = db.query(Attendance).filter(Attendance.employee_id == employee_id)

    if month:
        query = query.filter(Attendance.attendance_date.month == month)

    records = query.all()
    return records
