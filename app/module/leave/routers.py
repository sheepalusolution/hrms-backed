from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.module.leave import models, schemas

router = APIRouter()

@router.post("", response_model=schemas.LeaveOut)
def apply_leave(leave: schemas.LeaveCreate, db: Session = Depends(get_db)):
    new_leave = models.Leave(**leave.dict())
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave

@router.get("", response_model=List[schemas.LeaveOut])
def get_all_leaves(db: Session = Depends(get_db)):
    return db.query(models.Leave).all()
