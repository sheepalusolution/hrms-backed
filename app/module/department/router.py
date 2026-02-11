from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.module.department import models, schemas

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

# -----------------------------
# Create Department
# -----------------------------
@router.post("", response_model=schemas.DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

# -----------------------------
# Get All Departments
# -----------------------------
@router.get("", response_model=List[schemas.DepartmentOut])
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

# -----------------------------
# Get Department by ID
# -----------------------------
@router.get("{department_id}", response_model=schemas.DepartmentOut)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

# -----------------------------
# Update Department
# -----------------------------
@router.put("/{department_id}", response_model=schemas.DepartmentOut)
def update_department(department_id: int, department_data: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for key, value in department_data.dict(exclude_unset=True).items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)
    return department

# -----------------------------
# Delete Department
# -----------------------------
@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(department)
    db.commit()
    return {"detail": "Department deleted successfully"}
