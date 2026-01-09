from fastapi import FastAPI
from app.routers import auth, admin

app = FastAPI(title="HRMS Backend Auth Example")

app.include_router(auth.router)
app.include_router(admin.router)
