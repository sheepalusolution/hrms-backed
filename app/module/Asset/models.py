from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from app.core.database import Base
from sqlalchemy.orm import relationship
class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    asset_name = Column(String(100), nullable=False)
    status = Column(String(50))  # e.g., Assigned, Returned, Damaged
    employee_id = Column(Integer, ForeignKey("employees.id"))
    assigned_date = Column(Date)
    return_date = Column(Date)
    condition_on_return = Column(Text)
    quantity = Column(Integer, default=1)
     
    employee = relationship("Employee", back_populates="assets")