from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.core.audit_logger import log_auth_event
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password
from app.core.token import (
    create_access_token,
    create_tokens,
    generate_refresh_token,
    hash_refresh_token,
)
from app.module.auth.dependencies import get_current_user
from app.module.auth.models import RefreshToken, User
from app.module.auth.schemas import EmployeeCreate
from app.module.department.models import Department
from app.module.employee.models import Employee
from app.module.role.models import Role
from app.module.employee.models import EmployeeStatusEnum, EmployeeTypeEnum
router = APIRouter(tags=["Auth"])


# ------------------------
# REGISTER
# ------------------------
@router.post("/register")
def register_employee(data: EmployeeCreate, db: Session = Depends(get_db)):

    # 1. Department & Role lookup
    dept = db.query(Department).filter(Department.name.ilike(data.department_name)).first()
    role = db.query(Role).filter(Role.name.ilike(data.role_name)).first()
    if not dept or not role:
        raise HTTPException(status_code=400, detail="Invalid Department or Role name selected")

    # 2. Email check
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 3. Create auth user
    hashed_pwd = get_password_hash(data.password)
    new_user = User(
        email=data.email,
        password_hash=hashed_pwd,
        role_id=role.id,
        is_active=True
    )
    db.add(new_user)
    db.flush()  # ensures new_user.id is available

    # 4. Create employee
    new_employee = Employee(
        user_id=new_user.id,
        first_name=data.first_name,
        last_name=data.last_name,
        dob=data.dob,
        gender=data.gender,
        ph_no=data.ph_no,
        email=data.email,
        password=hashed_pwd,
        department_id=dept.id,
        role_id=role.id,
        join_date=data.join_date,
        end_date=data.end_date,
        employee_type=data.employee_type.value,  # enum -> string
        status=data.status.value if data.status else EmployeeStatusEnum.active.value,
        address=data.address,
        nationality=data.nationality,
    )

    db.add(new_employee)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {
        "message": "Employee Registered Successfully",
        "employee_email": new_employee.email,
        "department_name": dept.name,
        "role_name": role.name,
        "status": new_employee.status,
    }
# ------------------------
# LOGIN
# ------------------------
ROLE_MAP = {
    1: "user",
    2: "hr_admin",
    3: "employee",
    4: "superadmin",
    6: "finance",
    7: "manager",
    8: "recruiter",
}


@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    ip = request.client.host
    email = form_data.username
    password = form_data.password

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        log_auth_event(
            db,
            "LOGIN_FAILED",
            None,
            ip,
            description=f"Failed login attempt for {email}",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    log_auth_event(db, "LOGIN_SUCCESS", user.id, ip, role=str(user.role_id))

    role_name = ROLE_MAP.get(user.role_id, "user")

    payload = {
        "sub": user.email,
        "user_id": user.id,
        "role_id": user.role_id,
        "role_name": role_name,
    }

    access_token = create_access_token(payload)

    raw_refresh_token = generate_refresh_token()
    refresh_token_hash = hash_refresh_token(raw_refresh_token)

    db.add(RefreshToken(user_id=user.id, token_hash=refresh_token_hash))
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": raw_refresh_token,
        "role_name": role_name,
        "email": user.email,
    }


# ------------------------
# PROFILE
# ------------------------
@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "role_id": current_user.role_id}


# ------------------------
# REFRESH TOKEN
# ------------------------
@router.post("/refresh")
def refresh(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)):

    token_hash = hash_refresh_token(refresh_token)

    token_db = (
        db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    )

    if not token_db or token_db.is_revoked:
        if token_db:
            db.query(RefreshToken).filter(
                RefreshToken.user_id == token_db.user_id
            ).update({"is_revoked": True})
            db.commit()
        raise HTTPException(
            status_code=401, detail="Refresh token reuse detected. Session revoked."
        )

    user = db.query(User).filter(User.id == token_db.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    token_db.is_revoked = True  # revoke old token

    new_refresh_raw = generate_refresh_token()
    new_refresh_hash = hash_refresh_token(new_refresh_raw)
    db.add(RefreshToken(user_id=user.id, token_hash=new_refresh_hash))
    db.commit()

    tokens = create_tokens({"sub": user.email, "role_id": user.role_id})
    tokens["refresh_token"] = new_refresh_raw

    return tokens


# ------------------------
# LOGOUT
# ------------------------
@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    request: Request = None,
    db: Session = Depends(get_db),
):
    ip = request.client.host if request else "unknown"

    db.query(RefreshToken).filter(RefreshToken.user_id == current_user.id).update(
        {"is_revoked": True}
    )
    db.commit()

    log_auth_event(db, "LOGOUT", current_user.id, ip, role=str(current_user.role_id))

    return {"msg": "Successfully logged out"}
