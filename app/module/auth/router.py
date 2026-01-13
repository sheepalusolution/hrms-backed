from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.module.auth.models import User
from app.core.security import verify_password, get_password_hash
from app.core.token import create_tokens

router = APIRouter(tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # 1. Check if user already exists
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        raise HTTPException(
            status_code=400, 
            detail="A user with this email already exists."
        )
    
    # 2. Create the user
    # IMPORTANT: We do NOT use role="user" because 'role' is a relationship.
    # We use 'role_id' or leave it empty if your DB allows nulls.
    new_user = User(
        email=email,
        password_hash=get_password_hash(password),
        is_active=True,
        role_id=1  # Ensure a role with ID 1 exists in your 'roles' table
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return {"msg": "User created successfully", "email": email}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Payload for the JWT
    payload = {"sub": str(user.id), "role_id": user.role_id}
    return create_tokens(payload)