# app/utils/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.settings import JWTSettings
from app.schemas.pydatic_schemas import TokenData  # ✅ Correctly import this

security = HTTPBearer(auto_error=True)
jwt_settings = JWTSettings()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            jwt_settings.SECRET_KEY,
            algorithms=[jwt_settings.ALGORITHM]
        )

        email = payload.get("email")
        user_id = payload.get("user_id")

        if not email or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload missing required fields.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # ✅ Return a TokenData Pydantic model
        return TokenData(email=email, user_id=user_id)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
