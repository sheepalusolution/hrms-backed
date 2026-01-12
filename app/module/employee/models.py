from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class EmployeeTypeEnum(str, enum.Enum):
    full_time = "full_time"
    intern = "intern"
    contract = "contract"

class EmployeeStatusEnum(str, enum.Enum):
    active = "Active"
    resigned = "resigned"
    leave = "leave"

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    e_code = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date)
    gender = Column(String)
    ph_no = Column(String)
    email = Column(String)
    department_id = Column(Integer, ForeignKey("department.id"))
    designation_id = Column(Integer, ForeignKey("designation.id"))
    employee_type = Column(SQLEnum(EmployeeTypeEnum))
    join_date = Column(Date)
    end_date = Column(Date, nullable=True)
    status = Column(SQLEnum(EmployeeStatusEnum))
    address = Column(String)
    emergency_contact = Column(String)
    nationality = Column(String)

    # Relationships
    department = relationship(
        "Department",
        foreign_keys=[department_id],  # ✅ avoids AmbiguousForeignKeysError
        back_populates="employees"
    )
    designation = relationship("Designation", back_populates="employees")
    attendance = relationship("Attendance", back_populates="employee")
    leaves = relationship("Leave", back_populates="employee")
    payroll = relationship("Payroll", back_populates="employee")
    assets = relationship("Assets", back_populates="employee")
    users = relationship("User", back_populates="employee")
    documents = relationship("Document", back_populates="employee")