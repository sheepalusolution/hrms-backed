from datetime import date

from pydantic import BaseModel


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
        from_attribute = True
