from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.core.security import verify_password

router = APIRouter()

@router.post("/login")
def login(
    email: str = Form(..., description="User email"),
    password: str = Form(..., description="User password", password=True),  # <-- password hides input
    db: Session = Depends(get_db)
):
    # Fetch user
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    roles = [role.name for role in user.roles]

    return {
        "message": f"Welcome {email}!",
        "roles": roles
    }
