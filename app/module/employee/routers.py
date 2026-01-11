from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.module.employee import models, schemas

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

# -----------------------------
# Create Employee
# -----------------------------
@router.post("/", response_model=schemas.EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# -----------------------------
# Get All Employees
# -----------------------------
@router.get("/", response_model=List[schemas.EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    # Return only non-resigned employees by default
    return db.query(models.Employee).filter(models.Employee.status != models.EmployeeStatusEnum.resigned).all()

# -----------------------------
# Get Employee by ID
# -----------------------------
@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# -----------------------------
# Update Employee
# -----------------------------
@router.put("/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(employee_id: int, employee_data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee_data.dict(exclude_unset=True).items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee

# -----------------------------
# Soft Delete Employee (Mark as Resigned)
# -----------------------------
@router.delete("/{employee_id}", response_model=schemas.EmployeeOut)
def soft_delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Soft delete: mark as resigned
    employee.status = models.EmployeeStatusEnum.resigned
    db.commit()
    db.refresh(employee)
    return employee
