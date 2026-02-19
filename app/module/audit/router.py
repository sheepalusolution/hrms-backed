from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.audit import models, schemas
from app.module.auth.dependencies import get_current_user
from app.module.auth.models import User

router = APIRouter(tags=["Audit Logs"])


# 📌 Create audit log (internal use)
def create_audit_log(
    db: Session,
    user_id: int | None,
    action: str,
    table_name: str,
    record_id: int | None,
    description: str,
    ip_address: str | None,
):
    log = models.AuditLog(
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        description=description,
        ip_address=ip_address,
    )
    db.add(log)
    db.commit()


# 📌 Admin can view all audit logs
@router.get("/all", response_model=list[schemas.AuditLogOut])
def get_all_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role_id != 4:
        raise HTTPException(status_code=403, detail="Access denied")

    return db.query(models.AuditLog).order_by(
        models.AuditLog.timestamp.desc()
    ).all()


# 📌 Get logs for specific user
@router.get("/my", response_model=list[schemas.AuditLogOut])
def get_my_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logs = (
        db.query(models.AuditLog)
        .filter(models.AuditLog.user_id == current_user.id)
        .order_by(models.AuditLog.timestamp.desc())
        .all()
    )

    return logs

@router.get("/user/{user_id}", response_model=list[schemas.AuditLogOut])
def get_user_logs(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role_id != 4:
        raise HTTPException(status_code=403, detail="Access denied")

    return db.query(models.AuditLog).filter(
        models.AuditLog.user_id == user_id
    ).all()
