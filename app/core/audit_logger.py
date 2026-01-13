import logging
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.module.audit.models import AuditLog

# Setup File Logger
file_logger = logging.getLogger("secure_audit")
file_logger.setLevel(logging.INFO)
handler = logging.FileHandler("audit_secure.log")
handler.setFormatter(logging.Formatter("%(message)s"))
file_logger.addHandler(handler)

def log_auth_event(db: Session, action: str, user_id: str, ip: str, role: str = "N/A", description: str = None):
    # 1. Save to Database
    db_log = AuditLog(
        user_id=str(user_id),
        action=action,
        role=role,
        ip_address=ip,
        description=description
    )
    db.add(db_log)
    db.commit()

    # 2. Save to Secure File (JSON format for masking/parsing)
    file_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "user": user_id,
        "ip": ip,
        "role": role,
        "details": description
    }
    file_logger.info(json.dumps(file_entry))