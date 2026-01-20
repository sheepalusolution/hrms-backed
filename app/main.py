from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
# 🔥 Import all models first!
from app.module.auth.models import User
from app.module.role.models import Role
from app.module.employee.models import Employee
from app.module.department.models import Department
from app.module.designation.models import Designation
from app.module.Asset.models import Assets
from app.module.leave.models import Leave
from app.module.attendance.models import Attendance
from app.module.payroll.models import Payroll
from app.module.audit.models import AuditLog
from app.module.document.models import Document

# Import routers
from app.module.auth.router import router as auth_router
from app.module.role.routers import router as role_router
from app.module.employee.routers import router as employee_router
from app.module.Asset.router import router as asset_router
from app.module.department.router import router as department_router
from app.module.leave.routers import router as leave_router
from app.module.attendance.router import router as attendance_router
from app.module.payroll.router import router as payroll_router
from app.module.audit.router import router as audit_router


# FastAPI app
from fastapi import FastAPI
app = FastAPI(title="HRMS Backend")

# Include routers
app.include_router(auth_router, prefix="/auth")
# app.include_router(role_router, prefix="/role")
# app.include_router(employee_router, prefix="/employee")
# app.include_router(asset_router, prefix="/asset")
# app.include_router(department_router, prefix="/department")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Now SQLAlchemy knows all tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def Home():
    return {"message": "Welcome to Shepalu Solution HRMS API"}