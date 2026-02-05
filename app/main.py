from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import AuthMiddleware
from app.create_superadmin import create_superadmin
# 🔥 Import all models first!
from app.module.auth.models import User
from app.module.role.models import Role
from app.module.employee.models import Employee
from app.module.department.models import Department
from app.module.designation.models import Designation
from app.module.asset.models import Assets
from app.module.leave.models import Leave
from app.module.attendance.models import Attendance
from app.module.payroll.models import Payroll
from app.module.audit.models import AuditLog
from app.module.document.models import Document

# Import routers
from app.module.auth.router import router as auth_router
from app.module.role.routers import router as role_router
from app.module.employee.routers import router as employee_router
from app.module.asset.router import router as asset_router
from app.module.department.router import router as department_router
from app.module.leave.routers import router as leave_router
from app.module.attendance.router import router as attendance_router
from app.module.payroll.router import router as payroll_router
from app.module.audit.router import router as audit_router
from app.module.designation.router import router as designation_router

# FastAPI app
from fastapi import FastAPI
app = FastAPI(title="HRMS Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth_router, prefix="/auth")
app.include_router(role_router, prefix="/role")
app.include_router(employee_router, prefix="/employee")
# app.include_router(asset_router, prefix="/asset")
app.include_router(department_router, prefix="/department")
#  app.include_router(leave_router, prefix="/leave")
# app.include_router(attendance_router, prefix="/attendance")
# app.include_router(designation_router, prefix="/designations")
# 🔥 Now SQLAlchemy knows all tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def Home():
    return {"message": "Welcome to Shepalu Solution HRMS API"}

@app.on_event("startup")
def startup_event():
    
    print("Checking for Superadmin...")
    create_superadmin()
    