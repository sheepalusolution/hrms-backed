from fastapi import Depends, HTTPException, status
from app.core.deps import get_current_user

def role_required(allowed_roles: list):
    def checker(user=Depends(get_current_user)):
        if user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return user
    return checker
