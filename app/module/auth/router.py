from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.auth.models import User
from app.module.auth.schemas import TokenResponse
from app.core.security import verify_password, decode_token
from app.core.token import create_tokens
from app.core.roles import Role

router = APIRouter(prefix="/auth", tags=["Auth"])

# Use OAuth2PasswordBearer for token validation
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Login endpoint using form data
@router.post("/login", response_model=TokenResponse)
def login(
    email: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Authenticate user
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    payload = {
        "sub": str(user.id),
        "role": user.role.value
    }

    return create_tokens(payload)


# Get current user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).get(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# Role-based access decorator
def role_required(required_role: Role):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        return user
    return wrapper
