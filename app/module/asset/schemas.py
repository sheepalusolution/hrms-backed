# app/module/Asset/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


# Must match your SQLAlchemy Enum
class AssetStatusEnum(str, Enum):
    damaged = "Damaged"
    available = "Available"
    assigned = "Assigned"


class AssetBase(BaseModel):
    asset_name: str
    quantity: int = 1
    category: str 
    status: Optional[AssetStatusEnum] = AssetStatusEnum.available
    employee_id: Optional[int] = None
    assigned_date: Optional[date] = None
    return_date: Optional[date] = None


class AssetCreate(AssetBase):
    pass


class AssetOut(AssetBase):
    id: int

    class Config:
        from_attribute = True
