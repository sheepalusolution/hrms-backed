from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.payroll.models import Payroll
from app.module.payroll.schemas import PayrollGenerateRequest, PayrollResponse
from app.module.auth.dependencies import get_current_employee, get_superadmin
from app.module.auth.models import User

router = APIRouter(tags=["Payroll"])


# ✅ SUPER ADMIN ONLY
@router.post("/generate", response_model=PayrollResponse)
def generate_payroll(
    data: PayrollGenerateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin),
):
    existing = db.query(Payroll).filter(
        Payroll.employee_id == data.employee_id,
        Payroll.month == data.month,
        Payroll.year == data.year
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Payroll already exists")

    payroll = Payroll(**data.dict())

    db.add(payroll)
    db.commit()
    db.refresh(payroll)

    return payroll


# ✅ SUPER ADMIN ONLY
@router.get("/all", response_model=list[PayrollResponse])
def get_all_payroll(
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin),
):
    return db.query(Payroll).all()


# ✅ EMPLOYEE SELF VIEW
@router.get("/my", response_model=list[PayrollResponse])
def get_my_payroll(
    db: Session = Depends(get_db),
    current_employee = Depends(get_current_employee),
):
    return db.query(Payroll).filter(
        Payroll.employee_id == current_employee.id
    ).all()


# ✅ SUPER ADMIN ONLY
@router.get("/filter", response_model=list[PayrollResponse])
def filter_payroll(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin),
):
    return db.query(Payroll).filter(
        Payroll.month == month,
        Payroll.year == year
    ).all()