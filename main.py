
from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def graeting():
    return("Hello, World!")