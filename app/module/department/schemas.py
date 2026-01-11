from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -----------------------------
# Department Schemas
# -----------------------------
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: Optional[int] = None  # Can point to an Employee

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None

class DepartmentOut(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
    