from datetime import datetime, timedelta
from typing import Optional
import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
from Backend.models import User

load_dotenv()

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get JWT secret from environment
SECRET_KEY = os.getenv("JWT_SECRET", "zlgVAQq6/7GLjAvgvf/4T1NOnb+7BdOYMGFbx/hxsDY=")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days in minutes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    import logging
    logger = logging.getLogger(__name__)
    
    # Log the password and hash info for debugging (remove in production)
    logger.debug(f"Plain password length: {len(plain_password)} chars, {len(plain_password.encode('utf-8'))} bytes")
    logger.debug(f"Hashed password starts with: {hashed_password[:20] if hashed_password else 'None'}...")
    
    # Ensure we're working with the password that was used to create the hash
    # Bcrypt has a 72-byte limit, so we need to handle this consistently
    password_to_verify = plain_password
    
    # If the plain password is longer than 72 bytes, truncate it
    if len(plain_password.encode('utf-8')) > 72:
        logger.debug("Truncating password to 72 bytes for bcrypt compatibility")
        password_to_verify = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        logger.debug(f"Truncated password length: {len(password_to_verify)} chars, {len(password_to_verify.encode('utf-8'))} bytes")
    
    try:
        result = pwd_context.verify(password_to_verify, hashed_password)
        logger.debug(f"Password verification result: {result}")
        return result
    except ValueError as e:
        logger.error(f"ValueError in password verification: {str(e)}")
        # Handle bcrypt password length error
        if "password cannot be longer than 72 bytes" in str(e):
            # Truncate to 72 bytes and try again
            logger.debug("Retrying with 72-byte truncated password due to ValueError")
            truncated_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return pwd_context.verify(truncated_password, hashed_password)
        else:
            # Re-raise other ValueErrors
            logger.error(f"Non-bcrypt ValueError: {str(e)}")
            raise e
    except Exception as e:
        # Log the error for debugging (in production, be careful with logging)
        logger.error(f"Unexpected error in password verification: {str(e)}", exc_info=True)
        return False


def get_password_hash(password: str) -> str:
    """Generate a hash for the given password."""
    # Bcrypt has a 72-byte limit, so truncate if necessary before hashing
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # Handle bcrypt password length error
        if "password cannot be longer than 72 bytes" in str(e):
            # Ensure the password is properly truncated to 72 bytes
            truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return pwd_context.hash(truncated_password)
        else:
            # Re-raise other ValueErrors
            raise e


def authenticate_user(user: User, password: str) -> bool:
    """Authenticate a user by verifying their password."""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.debug(f"Starting authentication for user: {user.email}")
    logger.debug(f"Password hash type: {type(user.password_hash)}")
    logger.debug(f"Password hash starts with: {user.password_hash[:10] if user.password_hash else 'None'}")
    logger.debug(f"Input password length: {len(password)} chars, {len(password.encode('utf-8'))} bytes")
    
    is_valid = verify_password(password, user.password_hash)
    logger.debug(f"Password verification result: {is_valid}")
    
    return is_valid


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