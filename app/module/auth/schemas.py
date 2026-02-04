from typing import  Optional
from datetime import date
from pydantic import BaseModel, EmailStr

# ---------- REGISTER (Simplified) ----------
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    nationality: str
    address: str
    gender: str
    dob: date  # Date of Birth
    phone: str
    department_name: str
    deparment_id:int
    role_name: str
    role_id:int
    employee_type: str
    join_date: date
    end_date:date
    
# ---------- LOGIN ----------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ---------- TOKEN RESPONSE ----------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# ---------- TOKEN PAYLOAD (JWT DATA) ----------
class TokenPayload(BaseModel):
    sub: Optional[str] = None      # Stores user email
    role: Optional[str] = None     # Stores ROLE NAME (e.g., "superadmin")