from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from jose import JWTError
from services.auth import verify_token
from models import User

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to extract and validate user ID from JWT token.
    Returns the user ID if the token is valid, raises HTTPException otherwise.
    """
    token = credentials.credentials
    
    # Verify the token and extract payload
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id


def validate_user_id_match(url_user_id: str, token_user_id: str = Depends(get_current_user)) -> bool:
    """
    Validates that the user ID in the URL matches the user ID in the token.
    Raises HTTPException with 403 if they don't match.
    """
    if url_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )
    
    return True