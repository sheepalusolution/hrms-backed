from enum import Enum
from fastapi import Depends, HTTPException, status
from app.routers.auth import  user

class Roles(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

def role_required(*allowed_roles: Roles):
    def dependency(user=Depends(user)):
        if user.role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission"
            )
        return user
    return dependency
