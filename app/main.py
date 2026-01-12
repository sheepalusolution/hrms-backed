from fastapi import FastAPI
from app.module.auth.router import router as auth_router
from app.module.employee.routers import router as employees_router
from app.module.attendance.router import router as attendance_router
from app.module.department.router import router as department_router
from app.module.designation.router import router as designation_router
from app.module.leave.routers import router as leave_router
from app.module.Asset.router import router as asset_router  
from app.module.payroll.router import router as payroll_router
from app.module.audit.router import router as audit_router
from app.module.role.routers import router as role_router

from app.core.database import Base, engine
from app.module.employee.models import Employee
from app.module.auth.models import User
from app.module.attendance.models import Attendance
from app.module.department.models import Department
from app.module.designation.models import Designation
from app.module.leave.models import Leave
from app.module.Asset.models import Asset
from app.module.payroll.models import Payroll
from app.module.audit.models import AuditLog
from app.module.role.models import Role


app = FastAPI(title="HRMS Backend")

Base.metadata.create_all(bind=engine)

# Modular Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(employees_router, prefix="/employees", tags=["Employees"])
# app.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])

@app.get("/")
def home():
    return {"msg": "Welcome to HRMS Backend"}
