from fastapi import FastAPI
from app.models import documents, users
from app.models import department
from app.models import employees
from app.routers import auth
from app.database import Base, engine
from app.models import payroll, designation, attendance, assets, leaves, roles

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sheepalu Solutions")

@app.get("/")
def root():
    return {"message": "Welcome to Sheepalu Solutions!"}

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
