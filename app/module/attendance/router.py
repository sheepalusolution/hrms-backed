from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.module.audit import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.AuditLogOut)
def create_audit_log(log: schemas.AuditLogCreate, db: Session = Depends(get_db)):
    new_log = models.AuditLog(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/", response_model=List[schemas.AuditLogOut])
def get_audit_logs(db: Session = Depends(get_db)):
    return db.query(models.AuditLog).all()
