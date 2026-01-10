from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmployeeDocument(Base):
    __tablename__ = "employee_documents"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    document_type = Column(String(50))
    profile_photo = Column(Text)
    resume = Column(Text)

    employee = relationship("Employee", back_populates="documents")
