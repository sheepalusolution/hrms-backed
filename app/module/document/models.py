from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.core.database import Base
from sqlalchemy.orm import relationship
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    document_type = Column(String(50))
    profile_photo = Column(Text)
    resume = Column(Text)

    employee = relationship("Employee", back_populates="documents")