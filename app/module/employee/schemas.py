from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from enum import Enum

class EmployeeTypeEnum(str, Enum):
    full_time = "full_time"
    intern = "intern"
    contract = "contract"

class EmployeeStatusEnum(str, Enum):
    active = "Active"
    resigned = "resigned"
    leave = "leave"

class EmployeeBase(BaseModel):
    user_id: int
    e_code: str
    first_name: str
    last_name: str
    dob: Optional[date] = None
    gender: Optional[str] = None
    ph_no: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    employee_type: Optional[EmployeeTypeEnum] = None
    join_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[EmployeeStatusEnum] = None  # Enum for status
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    nationality: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    ph_no: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    employee_type: Optional[EmployeeTypeEnum] = None
    join_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[EmployeeStatusEnum] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    nationality: Optional[str] = None

class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
