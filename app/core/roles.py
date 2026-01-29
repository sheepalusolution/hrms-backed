from enum import Enum


class Role(str, Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# Optional helpers
def is_superadmin(role: Role) -> bool:
    return role == Role.SUPERADMIN

def is_admin(role: Role) -> bool:
    return role in (Role.ADMIN, Role.SUPERADMIN)

def is_user(role: Role) -> bool:
    return role == Role.USER
