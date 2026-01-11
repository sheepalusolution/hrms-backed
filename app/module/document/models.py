from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    upload_date = Column(Date, nullable=False)
    employee_id = Column(Integer, nullable=True)  # optional, can link to employee
