from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.auth.models import User
from app.module.auth.schemas import TokenResponse, UserCreate # Ensure UserCreate is in schemas
from app.core.security import verify_password, get_password_hash # Add get_password_hash
from app.core.token import create_tokens

router = APIRouter(tags=["Auth"])

# Defined at the top to avoid NameError
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- NEW REGISTRATION ENDPOINT ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if user already exists
    user_exists = db.query(User).filter(User.email == user_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=400, 
            detail="A user with this email already exists."
        )
    
    # 2. Hash the password and save
    new_user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role="user" # Default role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}

# --- UPDATED LOGIN ENDPOINT ---
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Search by email (form_data.username is the field name used by OAuth2)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    payload = {"sub": str(user.id), "role": user.role}
    return create_tokens(payload)