from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.token import verify_access_token

# ✅ Use a tuple for startswith
PUBLIC_ROUTES = ("/login", "/register", "/docs", "/openapi.json", "/")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Allow public routes
        print(f"AuthMiddleware: Incoming request to {request.url.path}")
        if request.url.path.startswith(PUBLIC_ROUTES):
            return await call_next(request)

        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        print(f"AuthMiddleware: Checking auth for {auth_header}")

        verify_result = (
            verify_access_token(auth_header.split(" ")[1]) if auth_header else None
        )

        if not verify_result:
            return JSONResponse(
                status_code=401, content={"detail": "Authorization token missing"}
            )

        # Store user info in request.state for downstream access
        request.state.user = verify_result

        return await call_next(request)
