from enum import Enum
from functools import wraps
from fastapi import Depends, HTTPException, status
from app.module.auth.dependencies import get_current_user

class Roles(str, Enum):
    ADMIN = "admin"
    HR = "hr"
    MANAGER = "manager"
    EMPLOYEE = "employee"


def role_required(*allowed_roles: Roles):
    """
    FastAPI dependency to enforce role-based access on endpoints.
    Usage:
    @app.get("/admin")
    def admin_route(user: User = Depends(role_required(Roles.ADMIN))):
        ...
    """
    def decorator(user=Depends(get_current_user)):
        if user.role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return user
    return decorator
