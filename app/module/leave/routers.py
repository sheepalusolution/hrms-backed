from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.auth.dependencies import get_current_employee, get_current_user
from app.module.leave.models import Leave, LeaveStatus
from app.module.leave.schemas import LeaveCreate, LeaveResponse, LeaveAction

router = APIRouter(tags=["Leaves"])

@router.get("/", response_model=list[LeaveResponse])
def get_all_leaves(db: Session = Depends(get_db)):
    leaves = db.query(Leave).order_by(Leave.start_date.desc()).all()
    return leaves

@router.post("/apply-leave")
def apply_leave(
    data: LeaveCreate,
    current_employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    # Ensure start_date and end_date are provided
    if not data.start_date or not data.end_date:
        raise HTTPException(status_code=400, detail="Start date and end date are required")

    new_leave = Leave(
        employee_id=current_employee.id,  # ✅ use logged-in employee
        reason=data.reason,
        start_date=data.start_date,
        end_date=data.end_date,
        status="Pending",
        approved_by=None
    )
    
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return {"message": "Leave applied successfully", "leave_id": new_leave.id}

@router.put("/{leave_id}")
def approve_leave(
    leave_id: int,
    action: LeaveAction,  # {"status": "Approved"}
    current_user = Depends(get_current_user),  # must be HR/Admin
    db: Session = Depends(get_db),
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.status != LeaveStatus.Pending:
        raise HTTPException(status_code=400, detail="Only pending leaves can be approved")

    if current_user.role.name not in ["hr_admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to approve leave")

    leave.status = LeaveStatus.Approved
    leave.approved_by = current_user.id

    db.commit()
    db.refresh(leave)

    return {"message": f"Leave {leave.id} approved", "status": leave.status}