from pydantic import BaseModel
from datetime import datetime

class AuditLogRead(BaseModel):
    user_id: int | None
    role: str | None
    action: str
    ip_address: str | None
    status: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
