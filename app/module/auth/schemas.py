from pydantic import BaseModel, EmailStr
from typing import Optional

# This is what was missing!
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
from pydantic import BaseModel, EmailStr
from typing import Optional

# ---------- REGISTER ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None   # email
    role_id: Optional[int] = None

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None