import os
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.document.models import Document
from app.module.document.schemas import DocumentResponse

router = APIRouter(tags=["Documents"])

UPLOAD_DIR = "media/documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)
@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    employee_id: int = Form(...),
    document_type: str = Form(None),
    profile_photo: UploadFile = File(None),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db),
):

    profile_path = None
    resume_path = None

    # ✅ Save profile photo
    if profile_photo:
        filename = f"{uuid4()}_{profile_photo.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(profile_photo.file.read())

        profile_path = filepath

    # ✅ Save resume
    if resume:
        filename = f"{uuid4()}_{resume.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(resume.file.read())

        resume_path = filepath

    document = Document(
        employee_id=employee_id,
        document_type=document_type,
        profile_photo=profile_path,
        resume=resume_path,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document
@router.get("/employee/{employee_id}", response_model=list[DocumentResponse])
def get_employee_documents(employee_id: int, db: Session = Depends(get_db)):

    docs = db.query(Document).filter(
        Document.employee_id == employee_id
    ).all()

    if not docs:
        raise HTTPException(status_code=404, detail="No documents found")

    return docs

