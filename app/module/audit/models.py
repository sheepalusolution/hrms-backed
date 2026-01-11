from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    action = Column(String, nullable=False)           # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    table_name = Column(String, nullable=False)      # employee, attendance, payroll, etc
    record_id = Column(Integer, nullable=True)       # affected row id
    description = Column(String, nullable=True)      # human readable message
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
