from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Skip public routes
        if request.url.path.startswith("/auth"):
            return await call_next(request)

        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=401, detail="Token missing")

        try:
            payload = jwt.decode(
                token.replace("Bearer ", ""),
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            request.state.user = payload  # store user in request

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return await call_next(request)
