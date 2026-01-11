from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.module.payroll import models, schemas

router = APIRouter(
    prefix="/payroll",
    tags=["Payroll"]
)

# Create a new payroll record
@router.post("/", response_model=schemas.PayrollOut)
def create_payroll(payroll: schemas.PayrollCreate, db: Session = Depends(get_db)):
    new_payroll = models.Payroll(
        employee_id=payroll.employee_id,
        salary=payroll.salary,
        month=payroll.month,
        year=payroll.year,
        currency=payroll.currency.value  # store enum as string
    )
    db.add(new_payroll)
    db.commit()
    db.refresh(new_payroll)
    return new_payroll


# Get all payroll records
@router.get("/", response_model=List[schemas.PayrollOut])
def get_payrolls(db: Session = Depends(get_db)):
    return db.query(models.Payroll).all()


# Get payroll record by ID
@router.get("/{payroll_id}", response_model=schemas.PayrollOut)
def get_payroll(payroll_id: int, db: Session = Depends(get_db)):
    payroll = db.query(models.Payroll).filter(models.Payroll.id == payroll_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    return payroll


# Delete payroll record
@router.delete("/{payroll_id}")
def delete_payroll(payroll_id: int, db: Session = Depends(get_db)):
    payroll = db.query(models.Payroll).filter(models.Payroll.id == payroll_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    db.delete(payroll)
    db.commit()
    return {"detail": "Payroll record deleted"}


# Optional: Update payroll record
@router.put("/{payroll_id}", response_model=schemas.PayrollOut)
def update_payroll(payroll_id: int, payroll_update: schemas.PayrollCreate, db: Session = Depends(get_db)):
    payroll = db.query(models.Payroll).filter(models.Payroll.id == payroll_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    
    payroll.employee_id = payroll_update.employee_id
    payroll.salary = payroll_update.salary
    payroll.month = payroll_update.month
    payroll.year = payroll_update.year
    payroll.currency = payroll_update.currency.value

    db.commit()
    db.refresh(payroll)
    return payroll
