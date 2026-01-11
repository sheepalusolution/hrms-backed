from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

# Optional: helper functions
def is_admin(role: Role) -> bool:
    return role == Role.ADMIN

def is_user(role: Role) -> bool:
    return role == Role.USER
