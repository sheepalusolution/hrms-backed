from fastapi import APIRouter
from app.core.roles import Roles, role_required
from fastapi import Depends

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def admin_dashboard(user=Depends(role_required(Roles.ADMIN))):
    return {"message": f"Welcome Admin {user['user_id']}"}
