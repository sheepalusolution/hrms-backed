
from pydantic import BaseModel, EmailStr

# Request schema for login
class LoginRequest(BaseModel):
    email: EmailStr  # validates proper email format
    password: str

# Response schema for login
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

# Optional: schema for creating a user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  
    is_active: bool = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True
