# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import auth, subscriptions
from fastapi import FastAPI, Form, File, UploadFile
from typing import Annotated


# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flutter App Backend")

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(subscriptions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flutter App Backend API"}


@app.post("/register")
async def register_user(email: str = Form(...), username: str = Form(...), password: str = Form(...)):
    return {"message": "User registered successfully", "email": email, "username": username}

