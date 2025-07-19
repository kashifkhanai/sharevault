from fastapi import APIRouter, HTTPException, status, Depends,Form
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone, timedelta
from jose import jwt

from app.schemas.pydatic_schemas import User, UserLogin, Token, UserRegisterResponse
from app.db.db_getter import get_db
from app.utils.helpers import hash_password, verify_password
from app.settings import JWTSettings

router = APIRouter(prefix="/auth")
jwt_settings = JWTSettings()


@router.post("/register", response_model=UserRegisterResponse)
async def register_user(payload: User, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Check if user exists by email
    existing_user = await db["users"].find_one({"email": payload.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = hash_password(payload.password)

    # Create new user document
    new_user = {
        "firstname": payload.firstname,
        "lastname": payload.lastname,
        "username": payload.username,
        "email": payload.email,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }

    result = await db["users"].insert_one(new_user)

    return UserRegisterResponse(
        message="User registered successfully",
        user_id=str(result.inserted_id),
        firstname=new_user["firstname"],
        lastname=new_user["lastname"],
        username=new_user["username"],
        email=new_user["email"]
    )


@router.post("/login", response_model=Token)
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # ✅ Find user by email (username is used for OAuth2's password flow)
    user = await db["users"].find_one({"email": email})

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # ✅ Create JWT token
    expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload_data = {
        "email": user["email"],
        "user_id": str(user["_id"]),
        "exp": expire
    }

    access_token = jwt.encode(
        claims=payload_data,
        key=jwt_settings.SECRET_KEY,
        algorithm=jwt_settings.ALGORITHM
    )

    # ✅ Return token response
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user["_id"]),
        email=user["email"]
    )