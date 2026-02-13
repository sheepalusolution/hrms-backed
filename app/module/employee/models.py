import enum

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.core.database import Base


class EmployeeTypeEnum(str, enum.Enum):
    full_time = ("full_time",)
    intern = ("intern",)

class EmployeeStatusEnum(str, enum.Enum):
    active = "Active"
    resigned = "resigned"
    leave = "leave"


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id")
    )  # Ensure this matches the 'users' table name
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date)
    gender = Column(String)
    ph_no = Column(String)
    email = Column(String)
    password = Column(String)
    department_id = Column(Integer, ForeignKey("department.id"))

    # FIX: Ensure "role.id" matches the __tablename__ in your Role model (often "roles")
    role_id = Column(Integer, ForeignKey("roles.id"))

    employee_type = Column(SQLEnum(EmployeeTypeEnum))
    join_date = Column(Date)
    end_date = Column(Date, nullable=True)
    status = Column(SQLEnum(EmployeeStatusEnum))
    address = Column(String)
    nationality = Column(String)

    # Relationships
    department = relationship(
        "Department", foreign_keys=[department_id], back_populates="employees"
    )

    # FIX: String reference "Role" must match the Class name in role/models.py
    role = relationship("Role", back_populates="employees")

    # FIX: Rename "users" to "user" (singular) for better readability
    user = relationship("User", back_populates="employee")

    attendance = relationship("Attendance", back_populates="employee")
    leaves = relationship("Leave", back_populates="employee")
    payroll = relationship("Payroll", back_populates="employee")
    assets = relationship("Assets", back_populates="employee")
    documents = relationship("Document", back_populates="employee")
