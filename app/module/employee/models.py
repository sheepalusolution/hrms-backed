from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    e_code = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    dob = Column(Date)
    gender = Column(String(40))
    phone_no = Column(String(20))
    email = Column(String(255))
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation_id = Column(Integer, ForeignKey("designations.id"))
    employee_type = Column(String(50))  # full_time, intern, contract
    join_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(100))  # active, resigned, leave
    address = Column(Text)
    emergency_contact = Column(String(50))
    nationality = Column(String(20))

    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    attendance = relationship("Attendance", back_populates="employee")
    payrolls = relationship("Payroll", back_populates="employee")
    documents = relationship("EmployeeDocument", back_populates="employee")
    assets = relationship("Asset", back_populates="employee")
    leaves = relationship("LeaveManage", back_populates="employee")
