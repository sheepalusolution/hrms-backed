from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.employee.models import Employee

router = APIRouter()

@router.post("/employees")
def create_employee(emp: Employee, db: Session = Depends(get_db)):
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

@router.get("/employees")
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()
