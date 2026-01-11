from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.module.role import models, schemas

router = APIRouter()

# Create a new role
@router.post("/", response_model=schemas.RoleOut)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = models.Role(name=role.name, description=role.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# Get all roles
@router.get("/", response_model=List[schemas.RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return db.query(models.Role).all()

# Get role by ID
@router.get("/{role_id}", response_model=schemas.RoleOut)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Delete role
@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"detail": "Role deleted"}
