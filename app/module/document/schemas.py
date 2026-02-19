from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DocumentBase(BaseModel):
    description: Optional[str] = None
    document_type: str

class DocumentCreate(DocumentBase):
    file: bytes  # optional if you want to upload file as bytes
    file_name: str  # original file name

class DocumentResponse(DocumentBase):
    id: int
    file_path: str
    upload_date: datetime
    employee_id: int

    class Config:
        from_attribute = True
