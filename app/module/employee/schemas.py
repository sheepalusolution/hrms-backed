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

from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from app.module.employee.models import EmployeeTypeEnum, EmployeeStatusEnum

class EmployeeBase(BaseModel):
    user_id: int 
    first_name: str
    last_name: str
    dob: Optional[date] = None
    gender: Optional[str] = None
    ph_no: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    # Changed from designation_id to role_id to match your DB
    role_id: Optional[int] = None 
    employee_type: Optional[EmployeeTypeEnum] = None
    join_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[EmployeeStatusEnum] = None
    address: Optional[str] = None
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
    # Changed from designation_id to role_id here as well
    role_id: Optional[int] = None 
    employee_type: Optional[EmployeeTypeEnum] = None
    join_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[EmployeeStatusEnum] = None
    address: Optional[str] = None
    nationality: Optional[str] = None

class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
