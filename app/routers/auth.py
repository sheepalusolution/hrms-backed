from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User
from app.core.security import verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Login
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    role_name = user.role.name if user.role else "NoRole"
    token = create_access_token({"user_id": user.id, "role": role_name})
    return {"access_token": token, "token_type": "bearer"}

# Role-based dependency
def role_required(allowed_roles: list):
    def wrapper(token: str = Depends(oauth2_scheme)):
        payload = decode_access_token(token)
        if not payload or payload.get("role") not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return payload
    return wrapper

# Test routes
@router.get("/admin-dashboard")
def admin_dashboard(user=Depends(role_required(["Admin"]))):
    return {"message": f"Welcome Admin!"}

@router.get("/employee-dashboard")
def employee_dashboard(user=Depends(role_required(["Employee", "Manager"]))):
    return {"message": f"Welcome {user['role']}!"}
