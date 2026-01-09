from pydantic import BaseModel, EmailStr, SecretStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr  # <-- this makes Swagger UI show dots for password

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str
