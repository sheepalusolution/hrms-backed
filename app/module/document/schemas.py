from pydantic import BaseModel
from datetime import date

class DocumentCreate(BaseModel):
    title: str
    description: str | None = None
    file_path: str
    upload_date: date
    employee_id: int | None = None

class DocumentOut(BaseModel):
    id: int
    title: str
    description: str | None
    file_path: str
    upload_date: date
    employee_id: int | None

    class Config:
        orm_mode = True
