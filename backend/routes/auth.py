from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from typing import Dict
from datetime import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from Backend.db import get_session
from Backend.models import User, UserCreate, UserLogin, UserResponse
from Backend.services.auth import get_password_hash, authenticate_user, create_access_token

router = APIRouter(tags=["authentication"])


@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    """
    Register a new user.
    Expects: {name: string, email: string, password: string}
    Returns: {user: object, token: string}
    """
    # Validate email format (basic validation)
    if "@" not in user_data.email or "." not in user_data.email.split("@")[1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password length
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    # Validate password length to ensure it doesn't exceed 72 bytes for bcrypt
    if len(user_data.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not exceed 72 bytes when encoded in UTF-8"
        )

    # Check if user already exists
    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    password_hash = get_password_hash(user_data.password)
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=password_hash
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    # Create access token
    access_token_expires = timedelta(days=7)  # 7 days as specified
    token_data = {
        "user_id": db_user.id,
        "email": db_user.email
    }
    token = create_access_token(data=token_data, expires_delta=access_token_expires)

    return UserResponse(user=db_user, token=token)


import logging

logger = logging.getLogger(__name__)

@router.post("/signin", response_model=UserResponse)
async def signin(user_credentials: UserLogin, session: AsyncSession = Depends(get_session)):
    """
    Authenticate user and return token.
    Expects: {email: string, password: string}
    Returns: {user: object, token: string}
    """
    try:
        # Find user by email
        logger.info(f"Attempting to sign in user: {user_credentials.email}")
        result = await session.execute(select(User).where(User.email == user_credentials.email))
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"Sign in failed: User not found: {user_credentials.email}")
            # Commit the transaction before raising the exception
            await session.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        logger.info(f"User found: {user.name}, verifying password...")
        
        # Log password length info (for debugging only, remove in production)
        password_bytes = len(user_credentials.password.encode('utf-8'))
        logger.info(f"Password length: {len(user_credentials.password)} chars, {password_bytes} bytes")
        logger.info(f"Password hash starts with: {user.password_hash[:20] if user.password_hash else 'None'}...")
        
        # Authenticate user with password
        try:
            authenticated = authenticate_user(user, user_credentials.password)
            logger.info(f"Password authentication result: {authenticated}")
        except ValueError as ve:
            logger.error(f"ValueError during password verification: {str(ve)}")
            await session.commit()  # Commit before raising
            if "password cannot be longer than 72 bytes" in str(ve):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password exceeds maximum length allowed"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password"
                )
        except Exception as e:
            logger.error(f"Unexpected error during password verification: {str(e)}")
            await session.commit()  # Commit before raising
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )

        if not authenticated:
            logger.warning(f"Sign in failed: Incorrect password for user: {user_credentials.email}")
            await session.commit()  # Commit before raising
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        logger.info(f"Sign in successful for user: {user.name}")
        
        # Create access token
        access_token_expires = timedelta(days=7)  # 7 days as specified
        token_data = {
            "user_id": user.id,
            "email": user.email
        }
        token = create_access_token(data=token_data, expires_delta=access_token_expires)

        # Commit the transaction before returning
        await session.commit()
        return UserResponse(user=user, token=token)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in signin endpoint: {str(e)}", exc_info=True)
        # Ensure transaction is committed before raising
        try:
            await session.rollback()
        except:
            pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )