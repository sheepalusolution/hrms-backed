from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.leave.models import Leave, LeaveStatus
from app.module.leave.schemas import LeaveCreate, LeaveResponse, LeaveAction

router = APIRouter(tags=["Leaves"])

@router.post("/", response_model=LeaveResponse)
def apply_leave(data: LeaveCreate, db: Session = Depends(get_db)):

    leave = Leave(
        employee_id=data.employee_id,
        reason=data.reason
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return leave

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

