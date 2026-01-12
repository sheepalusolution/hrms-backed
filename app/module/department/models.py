from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.module.employee.models import Employee
class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    manager_id = Column(Integer, ForeignKey("employee.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to designations
    designations = relationship("Designation", back_populates="department")

    # Relationship to employees in this department
    employees = relationship(
        "Employee",
        foreign_keys=lambda: [Employee.department_id],  
    )
