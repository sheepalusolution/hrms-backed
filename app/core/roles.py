from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    HR = "hr"
    