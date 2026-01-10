from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.audit.models import AuditLog
from app.module.audit.schemas import AuditLogRead
from app.core.roles import require_role

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@router.get("/", response_model=list[AuditLogRead])
def get_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
