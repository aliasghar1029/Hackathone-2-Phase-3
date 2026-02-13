from datetime import datetime, timedelta
from typing import Optional
import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
from models import User

load_dotenv()

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get JWT secret from environment
SECRET_KEY = os.getenv("JWT_SECRET", "zlgVAQq6/7GLjAvgvf/4T1NOnb+7BdOYMGFbx/hxsDY=")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days in minutes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    # Truncate password to 72 bytes if it exceeds the limit
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            # Ensure password is properly truncated to 72 bytes
            # Use byte-level truncation to avoid encoding issues
            truncated_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return pwd_context.verify(truncated_password, hashed_password)
        else:
            raise e


def get_password_hash(password: str) -> str:
    """Generate a hash for the given password."""
    # Truncate password to 72 bytes if it exceeds the limit
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            # Ensure password is properly truncated to 72 bytes
            # Use byte-level truncation to avoid encoding issues
            truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return pwd_context.hash(truncated_password)
        else:
            raise e


def authenticate_user(user: User, password: str) -> bool:
    """Authenticate a user by verifying their password."""
    if not verify_password(password, user.password_hash):
        return False
    return True


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with the given data."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return the payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """Extract user_id from a JWT token."""
    payload = verify_token(token)
    if payload:
        return payload.get("user_id")
    return None