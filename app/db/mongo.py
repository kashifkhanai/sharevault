
from app.settings import DatabaseSettings
import motor.motor_asyncio
from fastapi import HTTPException


class MongoDB: 
    def __init__(self,setting: DatabaseSettings) -> None:
        self.setting =setting
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(setting.MONGO_URL)
            self.db = self.client.get_database(setting.MONGO_INITDB_DATABASE)
        except Exception as  e:
            raise HTTPException(status_code=500,detail=f"Failed to Establish DB Connection: {e}")

