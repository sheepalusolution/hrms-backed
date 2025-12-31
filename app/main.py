from fastapi import FastAPI
from app.Auth_models import users
from app.Departments_module import department
from app.Employee_models import documents, employees
from app.routers import auth
from app.database import Base, engine
from app.Auth_models import payroll, designation, attendance, assets, leaves, roles

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sheepalu Solutions")

@app.get("/")
def root():
    return {"message": "Welcome to Sheepalu Solutions!"}

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
