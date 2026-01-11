from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from enum import Enum

# Enums matching your SQLAlchemy model
class EmployeeTypeEnum(str, Enum):
    full_time = "full_time"
    intern = "intern"
    contract = "contract"

class EmployeeStatusEnum(str, Enum):
    active = "Active"
    resigned = "resigned"
    leave = "leave"

# Request schema for creating/updating employee
class EmployeeCreate(BaseModel):
    user_id: int
    e_code: Optional[str] = None
    first_name: str
    last_name: str
    dob: Optional[date] = None
    gender: Optional[str] = None
    ph_no: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    employee_type: Optional[EmployeeTypeEnum] = EmployeeTypeEnum.full_time
    join_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[EmployeeStatusEnum] = EmployeeStatusEnum.active
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    nationality: Optional[str] = None

# Response schema for API output
class EmployeeResponse(BaseModel):
    id: int
    user_id: int
    e_code: Optional[str]
    first_name: str
    last_name: str
    dob: Optional[date]
    gender: Optional[str]
    ph_no: Optional[str]
    email: Optional[EmailStr]
    department_id: Optional[int]
    designation_id: Optional[int]
    employee_type: EmployeeTypeEnum
    join_date: Optional[date]
    end_date: Optional[date]
    status: EmployeeStatusEnum
    address: Optional[str]
    emergency_contact: Optional[str]
    nationality: Optional[str]

    model_config = {
        "from_attributes": True  
    }
