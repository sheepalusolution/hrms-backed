from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.module.auth.models import User
from app.core.security import get_password_hash

SUPERADMIN_EMAIL = "Admin123@gmail.com"
SUPERADMIN_PASSWORD = "Admin@123"
SUPERADMIN_ROLE_ID = 4  # SUPERADMIN

def create_superadmin():
    db: Session = SessionLocal()

    user = db.query(User).filter(User.email == SUPERADMIN_EMAIL).first()
    if user:
        print("✅ SuperAdmin already exists")
        return

    admin = User(
        email=SUPERADMIN_EMAIL,
        password_hash=get_password_hash(SUPERADMIN_PASSWORD),
        role_id=SUPERADMIN_ROLE_ID,
        is_active=True
    )

    db.add(admin)
    db.commit()
    db.close()

    print("🚀 SuperAdmin created successfully")
