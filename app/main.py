from fastapi import FastAPI
from app.core.database import Base, engine

# Import routers
from app.module.auth.router import router as auth_router
from app.module.role.routers import router as role_router
from app.module.employee.routers import router as employee_router
from app.module.Asset.router import router as asset_router
from app.module.department.router import router as department_router

# Initialize FastAPI app
app = FastAPI(title="HRMS Backend")

# Include routers
app.include_router(auth_router, prefix="/auth")
app.include_router(role_router, prefix="/role")
app.include_router(employee_router, prefix="/employee")
app.include_router(asset_router, prefix="/asset")
app.include_router(department_router, prefix="/department")

# Create all tables
Base.metadata.create_all(bind=engine)
