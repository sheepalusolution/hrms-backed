from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.auth.models import User
from app.module.employee.models import Employee
from app.module.leave.models import Leave
from app.module.leave.schemas import (
    LeaveCreate,
    LeaveOut,
    LeaveUpdateStatus,
)

router = APIRouter(tags=["Leaves"])


# =======================
# Create a Leave
# =======================
@router.post("/", response_model=LeaveOut, status_code=status.HTTP_201_CREATED)
def create_leave(leave: LeaveCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == leave.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_leave = Leave(employee_id=leave.employee_id, reason=leave.reason)
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave


# =======================
# Get All Leaves
# =======================
@router.get("/", response_model=List[LeaveOut])
def get_leaves(db: Session = Depends(get_db)):
    return db.query(Leave).all()


# =======================
# Get Leave by ID
# =======================
@router.get("/{leave_id}", response_model=LeaveOut)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave


# =======================
# Update Leave Status (Approve/Reject)
# =======================
@router.put("/{leave_id}/status", response_model=LeaveOut)
def update_leave_status(
    leave_id: int, status_update: LeaveUpdateStatus, db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    approver = db.query(User).filter(User.id == status_update.approved_by).first()
    if not approver:
        raise HTTPException(status_code=404, detail="Approver not found")

    leave.status = status_update.status
    leave.approved_by = status_update.approved_by

    db.commit()
    db.refresh(leave)
    return leave


# =======================
# Delete Leave
# =======================
@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    db.delete(leave)
    db.commit()
    return
