from pydantic import BaseModel


class AssetCreate(BaseModel):
    asset_name: str
    category: str
    quantity: int = 1
    value: float | None = None
    description: str | None = None


class AssetOut(BaseModel):
    id: int
    asset_name: str
    category: str
    quantity: int
    value: float | None
    description: str | None

    class Config:
        from_attribute = True
