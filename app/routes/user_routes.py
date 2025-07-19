# app/routes/user_routes.py

from fastapi import APIRouter, UploadFile, File, Request, Form, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.pydatic_schemas import UploadResponse, TokenData
from app.utils.helpers import generate_codes, get_expiry, save_file
from app.utils.authentication import get_current_user  # Make sure you're importing from the correct path
from app.db.db_getter import get_db
import os

router = APIRouter(prefix="/user")



########################
# 🔐 Upload File (JWT Required)
########################
@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    code_count: int = Form(5),
    expiry_hours: int = Form(24),
    current_user: TokenData = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Authenticated file upload.
    Generates multiple one-time download codes.
    """

    codes = generate_codes(code_count)
    path = save_file(file, codes[0])
    expires_at = get_expiry(expiry_hours)

    file_data = {
        "filename": file.filename,
        "path": path,
        "expires_at": expires_at,
        "downloads": 0,
        "codes": codes,
        "used_codes": [],
        "user_id": current_user.user_id,
        "uploaded_by": current_user.email
    }

    await db["files"].insert_one(file_data)

    base_url = str(request.base_url).rstrip("/")
    download_urls = [f"{base_url}/download/{code}" for code in codes]

    return {
        "message": "File uploaded successfully.",
        "download_urls": download_urls,
        "expires_at": expires_at
    }


########################
# 📁 My Uploads (JWT Required)
########################
@router.get("/my-uploads")
async def get_user_uploaded_files(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    """
    Show files uploaded by current user along with their usage stats.
    """

    cursor = db["files"].find({"user_id": current_user.user_id})
    uploads = []

    async for file in cursor:
        uploads.append({
            "filename": file["filename"],
            "downloads": file["downloads"],
            "used_codes": len(file["used_codes"]),
            "remaining_codes": len(file["codes"]) - len(file["used_codes"]),
            "expires_at": file["expires_at"]
        })

    return {
        "total_files": len(uploads),
        "uploads": uploads
    }
