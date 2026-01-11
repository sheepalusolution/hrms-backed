from pydantic import BaseModel

class AssetCreate(BaseModel):
    name: str
    category: str
    quantity: int = 1
    value: float | None = None
    description: str | None = None

class AssetOut(BaseModel):
    id: int
    name: str
    category: str
    quantity: int
    value: float | None
    description: str | None

    class Config:
        orm_mode = True
