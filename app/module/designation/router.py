from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.module.designation import models, schemas

router = APIRouter()

# -----------------------------
# Create Designation
# -----------------------------
@router.post("", response_model=schemas.DesignationOut, status_code=status.HTTP_201_CREATED)
def create_designation(designation: schemas.DesignationCreate, db: Session = Depends(get_db)):
    db_designation = models.Designation(**designation.dict())
    db.add(db_designation)
    db.commit()
    db.refresh(db_designation)
    return db_designation

# -----------------------------
# Get All Designations
# -----------------------------
@router.get("", response_model=List[schemas.DesignationOut])
def get_designations(db: Session = Depends(get_db)):
    return db.query(models.Designation).all()

# -----------------------------
# Get Designation by ID
# -----------------------------
@router.get("/{designation_id}", response_model=schemas.DesignationOut)
def get_designation(designation_id: int, db: Session = Depends(get_db)):
    designation = db.query(models.Designation).filter(models.Designation.id == designation_id).first()
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    return designation

# -----------------------------
# Update Designation
# -----------------------------
@router.put("/{designation_id}", response_model=schemas.DesignationOut)
def update_designation(designation_id: int, designation_data: schemas.DesignationUpdate, db: Session = Depends(get_db)):
    designation = db.query(models.Designation).filter(models.Designation.id == designation_id).first()
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    
    for key, value in designation_data.dict(exclude_unset=True).items():
        setattr(designation, key, value)

    db.commit()
    db.refresh(designation)
    return designation

# -----------------------------
# Delete Designation
# -----------------------------
@router.delete("/{designation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_designation(designation_id: int, db: Session = Depends(get_db)):
    designation = db.query(models.Designation).filter(models.Designation.id == designation_id).first()
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    
    db.delete(designation)
    db.commit()
    return {"detail": "Designation deleted successfully"}
