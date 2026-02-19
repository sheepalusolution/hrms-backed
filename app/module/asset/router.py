from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.Asset import models, schemas

router = APIRouter(tags=["Asset"])


# Create a new asset
# Create a new asset
@router.post("", response_model=schemas.AssetOut)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = db.query(models.Assets).filter(models.Assets.asset_name == asset.asset_name).first()
    if db_asset:
        raise HTTPException(status_code=400, detail="Asset already exists")
    new_asset = models.Assets(**asset.dict())
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset


# Get all assets
@router.get("", response_model=List[schemas.AssetOut])
def get_assets(db: Session = Depends(get_db)):
    return db.query(models.Assets).all()


# Get asset by ID
@router.get("/{asset_id}", response_model=schemas.AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(models.Assets).filter(models.Assets.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


# Delete asset
@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(models.Assets).filter(models.Assets.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(asset)
    db.commit()
    return {"detail": "Asset deleted"}
