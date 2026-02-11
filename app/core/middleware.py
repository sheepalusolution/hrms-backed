# app/core/middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from app.core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        PUBLIC_PATHS = [
            "/auth/register",
            "/auth/login",
            "/auth/refresh",
            "/docs",
            "/openapi.json",
            "/favicon.ico",
            "/attendance/clock-in",
            "/attendance/clock-out",
            "/"
        ]

        # ✅ Skip public routes and OPTIONS
        if request.url.path in PUBLIC_PATHS or request.method == "OPTIONS":
            return await call_next(request)

        # ✅ Read Bearer token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization token missing"}
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            # ✅ Save user info for routes
            request.state.user_id = payload.get("sub")
            request.state.role_id = payload.get("role_id")

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token expired"}
            )
        except jwt.PyJWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )

        return await call_next(request)
