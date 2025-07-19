import os
import asyncio
from datetime import datetime, timezone
from app.db.db_getter import get_db

async def cleanup_expired_files():
    db = get_db()  # This returns an AsyncIOMotorDatabase instance
    file_collection = db["files"]

    now = datetime.now(timezone.utc)
    cursor = file_collection.find({"expires_at": {"$lt": now}})

    deleted = 0
    async for file in cursor:
        path = file.get("path")
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"[CLEANUP] Failed to delete file: {path} — {e}")

        await file_collection.delete_one({"_id": file["_id"]})
        deleted += 1

    print(f"[CLEANUP] Deleted {deleted} expired files.")

# Optional: Run directly (only if executed as a script)
if __name__ == "__main__":
    asyncio.run(cleanup_expired_files())
