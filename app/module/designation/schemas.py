from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -----------------------------
# Designation Schemas
# -----------------------------
class DesignationBase(BaseModel):
    title: str
    grade: Optional[str] = None
    level: Optional[str] = None
    dep_id: Optional[int] = None  # Department ID

class DesignationCreate(DesignationBase):
    pass

class DesignationUpdate(BaseModel):
    title: Optional[str] = None
    grade: Optional[str] = None
    level: Optional[str] = None
    dep_id: Optional[int] = None

class DesignationOut(DesignationBase):
    id: int

    class Config:
        orm_mode = True
