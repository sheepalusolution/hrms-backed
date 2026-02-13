import json
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.module.audit.models import AuditLog

# Setup File Logger
file_logger = logging.getLogger("secure_audit")
file_logger.setLevel(logging.INFO)
handler = logging.FileHandler("audit_secure.log")
handler.setFormatter(logging.Formatter("%(message)s"))
file_logger.addHandler(handler)


def log_auth_event(
    db: Session,
    action: str,
    user_id: int | None,  # Changed to allow None for failed attempts
    ip: str,
    role: str = "N/A",
    table_name: str = "users",
    description: str = None,
):
    # 1. Save to Database
    db_log = AuditLog(
        user_id=user_id,  # Passed as int or None (NULL in DB)
        action=action,
        table_name=table_name,
        record_id=user_id,  # Usually the user_id for auth events
        role=role,
        ip_address=ip,
        description=description,
    )

    try:
        db.add(db_log)
        db.commit()
    except Exception as e:
        db.rollback()
        # Fallback log to file if database fails
        file_logger.error(f"DB Logging failed: {str(e)}")

    file_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "user_id": user_id,  # Will be null in JSON if None
        "ip": ip,
        "role": role,
        "table": table_name,
        "details": description,
    }
    file_logger.info(json.dumps(file_entry))
