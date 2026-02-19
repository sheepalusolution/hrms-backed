# FastAPI app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.create_superadmin import create_superadmin
from app.module.attendance.router import router as attendance_router

# 🔥 Import all models first!
# Import routers
from app.module.auth.router import router as auth_router
from app.module.department.router import router as department_router
from app.module.employee.routers import router as employee_router
from app.module.role.routers import router as role_router
from app.module.leave.routers import router as leave_router
from app.module.document.router import router as document_router
from app.module.payroll.router import router as payroll_router
from app.module.designation.router import router as designation_router
from app.module.audit.router import router as audit_log_router
from app.module.Asset.router import router as asset_router
from app.core.middleware import AuthMiddleware
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
app.include_router(role_router, prefix="/roles")

app.include_router(employee_router, prefix="/employees")
app.include_router(asset_router, prefix="/asset")
app.include_router(department_router, prefix="/departments")
# app.include_router(payroll_router, prefix="/payrolls")
app.include_router(attendance_router, prefix="/attendances")
app.include_router(leave_router, prefix="/leaves")
app.include_router(document_router, prefix="/documents")
app.include_router(designation_router, prefix="/designations")
app.include_router(audit_log_router, prefix="/audit-logs")
# 🔥 Now SQLAlchemy knows all tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def Home():
    return {"message": "Welcome to Shepalu Solution HRMS API"}


@app.on_event("startup")
def startup_event():

    print("Checking for Superadmin...")
    create_superadmin()
