from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import FileResponse
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.pydatic_schemas import FileInfoResponse
from app.db.db_getter import get_db
import os

router = APIRouter()


########################
# 🔹 File Info Route
########################
@router.get("/file-info/{code}", response_model=FileInfoResponse)
async def get_file_info(
    code: str,
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # 🔍 Try to find any file containing the code (even if used)
    file_data = await db["files"].find_one({"codes": code})

    if not file_data:
        raise HTTPException(status_code=404, detail="Invalid download code.")

    # 🕓 Check expiry
    expires_at = file_data["expires_at"]
    now = datetime.now(timezone.utc)

    if expires_at.tzinfo is None or expires_at.tzinfo.utcoffset(expires_at) is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if now > expires_at:
        raise HTTPException(status_code=410, detail="This file has expired.")

    # ✅ Check if code is already used
    if code in file_data["used_codes"]:
        raise HTTPException(status_code=410, detail="This code has already been used.")

    # 🏗️ Build the download URL
    base_url = str(request.base_url).rstrip("/")
    full_url = f"{base_url}/download/{code}"

    return {
        "filename": file_data["filename"],
        "expires_at": expires_at,
        "downloads": file_data["downloads"],
        "download_url": full_url
    }


########################
# 🔹 Download Route
########################
@router.get("/download/{code}")
async def download_file(
    code: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # 🧠 Find file using code
    file_data = await db["files"].find_one({"codes": code})

    if not file_data:
        raise HTTPException(status_code=404, detail="Invalid or expired code.")

    # ✅ Handle timezone-awareness
    expires_at = file_data["expires_at"]
    if expires_at.tzinfo is None or expires_at.tzinfo.utcoffset(expires_at) is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    # 🚫 Expiry check
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=410, detail="File has expired.")

    # 🚫 Already used code?
    if code in file_data["used_codes"]:
        raise HTTPException(status_code=410, detail="Code already used.")

    # ✅ Mark code as used & increment download count
    await db["files"].update_one(
        {"_id": file_data["_id"]},
        {
            "$push": {"used_codes": code},
            "$inc": {"downloads": 1}
        }
    )

    # 🧹 Cleanup if all codes are used
    used = file_data["used_codes"] + [code]
    if set(used) == set(file_data["codes"]):
        if os.path.exists(file_data["path"]):
            os.remove(file_data["path"])
        await db["files"].delete_one({"_id": file_data["_id"]})
        print(f"[CLEANUP] File '{file_data['filename']}' deleted (all codes used).")

    # 📦 Return the file
    return FileResponse(
        path=file_data["path"],
        filename=file_data["filename"],
        media_type="application/octet-stream"
    )
