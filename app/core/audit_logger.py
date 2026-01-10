from datetime import datetime
from fastapi import Request
import logging

# Configure basic logger
logger = logging.getLogger("audit_logger")
logger.setLevel(logging.INFO)

# Optional: write to file
file_handler = logging.FileHandler("audit.log")
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_audit(
    user_id: int,
    role: str,
    action: str,
    ip_address: str | None = None,
):
    """
    Logs authentication and authorization events
    """
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "role": role,
        "action": action,
        "ip": ip_address
    }

    # Log to console & file
    logger.info(log_entry)
