from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    value = Column(Float, nullable=True)
    description = Column(String, nullable=True)