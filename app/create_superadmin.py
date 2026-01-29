from app.core.database import SessionLocal
from app.module.auth.models import User
from app.module.role.models import Role
from app.core.security import get_password_hash

EMAIL = "superadmin@hrms.com"
PASSWORD = "SuperAdmin@123"

db = SessionLocal()

try:
    # 1️⃣ Ensure SUPERADMIN role exists
    role = db.query(Role).filter(Role.name == "SUPERADMIN").first()
    if not role:
        role = Role(name="SUPERADMIN")
        db.add(role)
        db.commit()
        db.refresh(role)
        print("✅ SUPERADMIN role created")

    # 2️⃣ Check if superadmin already exists
    user = db.query(User).filter(User.email == EMAIL).first()
    if user:
        print("⚠️ SuperAdmin already exists")
        exit()

    # 3️⃣ Create superadmin user
    superadmin = User(
        email=EMAIL,
        password_hash=get_password_hash(PASSWORD),
        role_id=role.id,
        is_active=True
    )

    db.add(superadmin)
    db.commit()

    print(" SuperAdmin created successfully")
    print(" Email:", EMAIL)
    print(" Password:", PASSWORD)

except Exception as e:
    db.rollback()
    print(" Error:", e)

finally:
    db.close()
