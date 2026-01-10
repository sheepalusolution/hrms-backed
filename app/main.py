from fastapi import FastAPI
from app.module.auth.router import router as auth_router
from app.module.employee.router import router as employees_router
from app.module.attendance.router import router as attendance_router

app = FastAPI(title="HRMS Backend")

# Modular Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(employees_router, prefix="/employees", tags=["Employees"])
app.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])

@app.get("/")
def home():
    return {"msg": "Welcome to HRMS Backend"}
