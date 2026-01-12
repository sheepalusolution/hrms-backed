from pydantic import BaseModel
from datetime import datetime

class AuditLogCreate(BaseModel):
    user_id: int | None = None
    action: str
    details: str | None = None

class AuditLogOut(BaseModel):
    id: int
    user_id: int | None
    action: str
    timestamp: datetime
    details: str | None

    class Config:
        from_attribute = True
