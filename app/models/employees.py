from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey, Text, Interval
from sqlalchemy.orm import relationship
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    e_code = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    
    gender = Column(String(40))
    ph_no = Column(String(20))
    email_official = Column(String(255), unique=True)
    email_personal = Column(String(255), unique=True)
    
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation_id = Column(Integer, ForeignKey("designations.id"))
    
    join_date = Column(Date)
    employee_type = Column(String(250))  # full_time, intern, contract
    
    address_permanent = Column(Text)
    address_current = Column(Text)
    emergency_contact = Column(String(50))
    nationality = Column(String(20))
    
    status = Column(String(50))  # Active, Inactive
  
    attendance = relationship("Attendance", back_populates="employee")
    assets = relationship("Asset", back_populates="employee")
    leaves = relationship("Leave", back_populates="employee")
    payrolls = relationship("Payroll", back_populates="employee")
    user = relationship("User", back_populates="employee")
    documents = relationship("EmployeeDocument", back_populates="employee")
    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")