# [Task]: T-008
# [From]: speckit.plan §8

from fastapi import Header, HTTPException, Depends
from ..services.auth import verify_token

async def get_current_user(authorization: str = Header(None)) -> str:
    """Extract and verify JWT, return user_id"""
    if not authorization:
        raise HTTPException(401, "Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    if not payload:
        raise HTTPException(401, "Invalid or expired token")

    return payload["user_id"]

async def verify_user_id(user_id: str, current_user: str = Depends(get_current_user)):
    """Verify that URL user_id matches JWT user_id"""
    if user_id != current_user:
        raise HTTPException(403, "Access forbidden")
    return user_id