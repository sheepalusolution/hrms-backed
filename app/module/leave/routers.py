from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.leave.models import Leave, LeaveStatus
from app.module.leave.schemas import LeaveCreate, LeaveResponse, LeaveAction

router = APIRouter(tags=["Leaves"])

@router.post("/apply-leave")
def apply_leave(data: LeaveCreate, db: Session = Depends(get_db)):
    # Ensure data.start_date and data.end_date are not None
    if not data.start_date or not data.end_date:
        raise HTTPException(status_code=400, detail="Start date and end date are required")

    new_leave = Leave(
        employee_id=data.employee_id,
        reason=data.reason,
        start_date=data.start_date, # Make sure these match the schema fields
        end_date=data.end_date,
        status="Pending",
        approved_by=None # This is fine as null initially
    )
    
    db.add(new_leave)
    db.commit()
    return {"message": "Leave applied successfully"}

@router.get("/", response_model=list[LeaveResponse])
def get_all_leaves(db: Session = Depends(get_db)):
    return db.query(Leave).all()

@router.get("/employee/{employee_id}", response_model=list[LeaveResponse])
def get_employee_leaves(employee_id: int, db: Session = Depends(get_db)):

    leaves = db.query(Leave).filter(
        Leave.employee_id == employee_id
    ).all()

    return leaves

@router.put("/{leave_id}", response_model=LeaveResponse)
def leave_action(
    leave_id: int,
    data: LeaveAction,
    db: Session = Depends(get_db),
):

    leave = db.query(Leave).filter(Leave.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.status = data.status

    # ⚠️ Replace with current logged-in user ID
    leave.approved_by = 1

    db.commit()
    db.refresh(leave)

    return leave

