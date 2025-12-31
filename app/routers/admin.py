from fastapi import APIRouter, Depends
from app.core.roles import role_required

router = APIRouter(prefix="/admin", tags=["Admin"])

# Admin only
@router.get("/dashboard")
def admin_dashboard(user=Depends(role_required(["Admin"]))):
    return {"message": "Admin Dashboard"}

# HR + Manager
@router.get("/employees")
def view_employees(user=Depends(role_required(["HR", "Manager"]))):
    return {"message": "Employee List"}
