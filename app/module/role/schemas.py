from pydantic import BaseModel

class RoleCreate(BaseModel):
    name: str
    description: str | None = None

class RoleOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        orm_mode = True
