from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuditLogBase(BaseModel):
    action: str
    table_name: str
    record_id: Optional[int]
    description: Optional[str]
    ip_address: Optional[str]


class AuditLogCreate(AuditLogBase):
    user_id: Optional[int]


class AuditLogOut(AuditLogBase):
    id: int
    user_id: Optional[int]
    timestamp: datetime

    class Config:
        from_attributes = True
