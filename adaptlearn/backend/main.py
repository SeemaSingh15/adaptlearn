import sys
import os

# Ensure backend directory is in path for imports to work if run from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.session import engine
from db.base import Base
from routers import auth, users, learning
from config import settings

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AdaptLearn AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(learning.router, prefix="/learn", tags=["learning"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AdaptLearn AI API"}
