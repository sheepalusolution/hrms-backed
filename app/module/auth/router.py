from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.module.auth.models import User
from app.module.auth.schemas import TokenResponse
from app.core.security import verify_password, decode_token
from app.core.token import create_tokens
from app.core.roles import Role

# 1. Initialize the router
router = APIRouter(tags=["Auth"]) # Removed prefix="/auth" here to avoid the /auth/auth issue

# 2. Define oauth2_scheme at the TOP to fix NameError
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 3. Login endpoint using the standard OAuth2 form
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # OAuth2PasswordRequestForm uses 'username' field to hold the email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    payload = {
        "sub": str(user.id),
        "role": user.role.value
    }

    return create_tokens(payload)

# 4. Get current user
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

# 5. Role-based access
def role_required(required_role: Role):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        return user
    return wrapper