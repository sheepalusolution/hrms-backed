import enum

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.core.database import Base


class AssetStatusEnum(str, enum.Enum):
    damaged = "Damaged"
    available = "Available"
    assigned = "Assigned"


class Assets(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    asset_name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)

    status = Column(SQLEnum(AssetStatusEnum), default=AssetStatusEnum.available)

    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=True)
    assigned_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    condition_on_return = Column(Text, nullable=True)

    employee = relationship("Employee", back_populates="assets")
