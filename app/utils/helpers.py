import os
import random
import string
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

# 🔹 Generate expiry time (default is 24 hours from now, in UTC)
def get_expiry(hours: int = 24) -> datetime:
    """
    Returns a timezone-aware datetime object for file expiry.
    """
    return datetime.now(timezone.utc) + timedelta(hours=hours)


# 🔸 Save file to 'uploads/' folder with a unique filename
def save_file(file, code: str) -> str:
    """
    Saves the uploaded file with a new name using the code.
    Returns the full file path.
    """
    # Get original file extension (e.g., .pdf, .jpg)
    filename = file.filename
    ext = filename.split('.')[-1] if '.' in filename else 'bin'
    new_filename = f"{code}.{ext}"

    # Ensure uploads folder exists
    os.makedirs("uploads", exist_ok=True)

    # Build full path and write file
    file_path = os.path.join("uploads", new_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path


# 🔹 Generate a list of unique random codes
def generate_codes(count: int, length: int = 6) -> list[str]:
    """
    Generates a list of unique alphanumeric codes.
    """
    codes = set()
    while len(codes) < count:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        codes.add(code)
    return list(codes)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

