from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from app.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # -------------------------------
        # Public endpoints (NO TOKEN)
        # -------------------------------
        PUBLIC_PATHS = [
            "/auth/login",
            "/auth/refresh",
            "/docs",
            "/openapi.json",
            "/"
        ]

        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # -------------------------------
        # Get Authorization header
        # -------------------------------
        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization token missing"}
            )

        token = auth.split(" ")[1]

        # -------------------------------
        # Verify ACCESS token
        # -------------------------------
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            # Save user info for controllers
            request.state.user_id = payload.get("sub")
            request.state.role = payload.get("role")

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
