from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String,Text, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    file_path = Column(String)  # or Text
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False) 
    employee_id = Column(Integer, ForeignKey("employee.id"))
    document_type = Column(String(50))

    employee = relationship("Employee", back_populates="documents")

