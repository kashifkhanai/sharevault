# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routes.router import api_router  
from app.utils.cleanup import cleanup_expired_files
from apscheduler.schedulers.background import BackgroundScheduler
import os

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[STARTUP] Checking for expired files to delete...")
    cleanup_expired_files()
    scheduler.add_job(cleanup_expired_files, 'interval', minutes=60)
    scheduler.start()
    yield
    print("[SHUTDOWN] Stopping the scheduler...")
    scheduler.shutdown()

# Ensure uploads directory exists
if not os.path.exists("uploads"):
    os.mkdir("uploads")

app = FastAPI(
    title="ShareVault API",
    description="A file sharing API with user authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(api_router)
########################
# 🔹 Root Route (Public)
########################
@app.get("/", tags=["Main Root"])
async def root():
    return {"message": "Welcome to ShareVault File Sharing API"}

