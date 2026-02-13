from typing import Optional

from pydantic import BaseModel


# =========================
# BASE
# =========================
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


# =========================
# CREATE
# =========================
class RoleCreate(RoleBase):
    pass


# =========================
# UPDATE
# =========================
class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# =========================
# RESPONSE
# =========================
class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True
