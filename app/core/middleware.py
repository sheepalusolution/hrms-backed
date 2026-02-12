from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from app.core.config import settings
from app.module.employee.models import Employee
from app.core.database import get_db
from sqlalchemy.orm import Session

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for login route
        if request.url.path in ["/auth/login", "/auth/refresh"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization token missing")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email = payload.get("sub")
            role_name = payload.get("role_name")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Attach employee/user info to request.state
        db: Session = next(get_db())
        employee = db.query(Employee).filter(Employee.email == email).first()
        if not employee:
            raise HTTPException(status_code=401, detail="Unauthorized: employee not found")

        request.state.employee = employee
        request.state.role_name = role_name

        response = await call_next(request)
        return response
