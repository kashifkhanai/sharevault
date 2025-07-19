
from pydantic import BaseModel, EmailStr, Field, field_validator,model_validator
from typing import Annotated, Optional
from enum import Enum
from datetime import datetime
from pydantic import ConfigDict
import re

class UploadResponse(BaseModel):
    message: str
    download_urls: list[str]     # 👈 This must match your response return key
    expires_at: datetime


class FileInfoResponse(BaseModel):
    filename: str
    expires_at: datetime
    downloads: int
    download_url: str
    


######################## Auth Models ####################################################################

    
# --- Regex for password ---
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"

# --- User Register Schema ---   
class User(BaseModel):
    firstname: Annotated[str, Field(..., description="First name is required")]
    lastname: Optional[str] = Field(default=None, description="Last name is optional")
    username: Annotated[
        str,
        Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$", description="Only letters, numbers, underscores")
    ]
    email: EmailStr
    password: str

    # Custom validator for password
    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                "Password must be at least 8 characters long, include uppercase, "
                "lowercase, number, and special character."
            )
        return value
    
class UserRegisterResponse(BaseModel):
    message: str
    user_id: str
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    
    
# --- User Login Schema ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    

################## Token ################################################################
class TokenData(BaseModel):
    user_id: str           # ✅ MongoDB _id (string form)
    email: str             # ✅ Authenticated user email
    exp: Optional[int] = None 

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str
    
    
