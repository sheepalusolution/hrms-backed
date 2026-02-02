from typing import  Optional
from pydantic import BaseModel, EmailStr

# ---------- REGISTER (Simplified) ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role_name: str  
    
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