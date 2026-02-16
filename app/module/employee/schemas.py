from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


# --- ENUMS ---
class EmployeeTypeEnum(str, Enum):
    full_time = "full_time"
    intern = "intern"


class EmployeeStatusEnum(str, Enum):
    active = "Active"
    resigned = "resigned"
    leave = "leave"


# --- BASE SCHEMA ---
class EmployeeBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    dob: Optional[date] = None
    gender: Optional[str] = None
    ph_no: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    role_id: Optional[int] = None
    employee_type: Optional[EmployeeTypeEnum] = None
    join_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[EmployeeStatusEnum] = None
    address: Optional[str] = None
    nationality: Optional[str] = None


# --- CREATE SCHEMA ---
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    dob: date
    gender: str
    ph_no: str
    email: str
    password: str
    department_name: str
    role_name: str
    join_date: date
    end_date: Optional[date] = None
    employee_type: EmployeeTypeEnum = EmployeeTypeEnum.full_time  # default
    address: Optional[str] = None
    nationality: Optional[str] = None
    status: EmployeeStatusEnum = EmployeeStatusEnum.active  # default


# --- UPDATE SCHEMA ---
class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    ph_no: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    role_id: Optional[int] = None
    employee_type: Optional[EmployeeTypeEnum] = None
    join_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[EmployeeStatusEnum] = None
    address: Optional[str] = None
    nationality: Optional[str] = None


# --- OUTPUT SCHEMA ---
class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
