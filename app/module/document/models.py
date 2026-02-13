from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    document_type = Column(String(50))
    profile_photo = Column(Text)
    resume = Column(Text)

    employee = relationship("Employee", back_populates="documents")
