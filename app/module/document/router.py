from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app.module.document import models, schemas

router = APIRouter()

# Create a new document
@router.post("", response_model=schemas.DocumentOut)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    new_doc = models.Document(**document.dict())
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

# Get all documents
@router.get("", response_model=List[schemas.DocumentOut])
def get_documents(db: Session = Depends(get_db)):
    return db.query(models.Document).all()

# Get document by ID
@router.get("/{document_id}", response_model=schemas.DocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

# Delete document
@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"detail": "Document deleted"}
