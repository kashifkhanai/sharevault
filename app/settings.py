from pydantic_settings import BaseSettings
from datetime import timezone

class APISettings(BaseSettings):
    TIME_ZONE: timezone = timezone.utc
    APP_VERSION: str ="1.0.0"
    APP_NAME: str ="Job Tracker"
    API_PREFIX:str = ""
    IS_DEBUG:bool =True

    class Config:
        env_file = '.env'
        extra = "ignore"

class JWTSettings(BaseSettings):   
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        extra = "ignore"


class DatabaseSettings(BaseSettings):
    MONGO_URL: str
    MONGO_INITDB_DATABASE: str

    class Config:
        env_file = ".env"
        extra = "ignore"
        
        
def get_settings():
    return DatabaseSettings()


