from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.auth.dependencies import get_current_employee, get_current_user
from app.module.leave.models import Leave, LeaveStatus, LeaveDayType
from app.module.leave.schemas import LeaveCreate, LeaveResponse, LeaveAction

router = APIRouter(tags=["Leaves"])


# 🔹 Get all leaves
@router.get("/", response_model=list[LeaveResponse])
def get_all_leaves(db: Session = Depends(get_db)):
    leaves = db.query(Leave).order_by(Leave.start_date.desc()).all()
    return leaves


# 🔹 Apply leave
@router.post("/apply-leave", response_model=LeaveResponse)
def apply_leave(
    data: LeaveCreate,
    current_employee=Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    # Validate dates
    if not data.start_date or not data.end_date:
        raise HTTPException(status_code=400, detail="Start date and end date are required")

    # Create new leave
    new_leave = Leave(
        employee_id=current_employee.id,
        reason=data.reason,
        start_date=data.start_date,
        end_date=data.end_date,         # ✅ Leave type
        day_type=data.day_type,              # ✅ Half/Full Day
        status=LeaveStatus.Pending,
        approved_by=None
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave


# 🔹 Approve / Reject leave
@router.put("/{leave_id}", response_model=LeaveResponse)
def approve_leave(
    leave_id: int,
    action: LeaveAction,  # {"status": "Approved"} or {"status": "Rejected"}
    current_user=Depends(get_current_user),  # must be HR/Admin
    db: Session = Depends(get_db),
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != LeaveStatus.Pending:
        raise HTTPException(status_code=400, detail="Only pending leaves can be approved or rejected")

    if current_user.role.name not in ["hr_admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to approve/reject leave")

    leave.status = action.status
    leave.approved_by = current_user.id

    db.commit()
    db.refresh(leave)

    return leave
