import os
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.document.models import Document
from app.module.document.schemas import DocumentResponse
from app.module.auth.dependencies import get_current_user

router = APIRouter(tags=["Documents"])

UPLOAD_DIR = "media/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    description: str = Form(None),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    employee_id = current_user.id

    # Save file
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    document = Document(
        description=description,
        document_type=document_type,
        file_path=file_path,
        employee_id=employee_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.get("/my-documents", response_model=list[DocumentResponse])
def get_my_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    employee_id = current_user.id
    docs = db.query(Document).filter(Document.employee_id == employee_id).all()

    if not docs:
        raise HTTPException(status_code=404, detail="No documents found")

    return docs
