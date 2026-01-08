from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class EmployeeDocument(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    document_type = Column(String(50))
    file_path = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    employee = relationship("Employee", back_populates="documents")