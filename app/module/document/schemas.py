from typing import Optional
from pydantic import BaseModel, ConfigDict


# 🔹 Create document (while uploading)
class DocumentCreate(BaseModel):
    employee_id: int
    document_type: Optional[str] = None


# 🔹 Response schema
class DocumentResponse(BaseModel):
    id: int
    employee_id: int
    document_type: Optional[str]
    profile_photo: Optional[str]
    resume: Optional[str]

    model_config = ConfigDict(from_attributes=True)
