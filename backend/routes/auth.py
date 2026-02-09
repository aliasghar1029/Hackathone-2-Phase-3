# [Task]: T-007
# [From]: speckit.plan §3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session
from ..db import get_session
from ..services import auth

router = APIRouter(prefix="/api/auth", tags=["auth"])

class SignupRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user: dict
    token: str

@router.post("/signup", response_model=AuthResponse)
def signup(data: SignupRequest, session: Session = Depends(get_session)):
    try:
        result = auth.signup(session, data.email, data.name, data.password)
        # Convert user object to dict for serialization
        user_dict = {
            "id": result["user"].id,
            "email": result["user"].email,
            "name": result["user"].name,
            "created_at": result["user"].created_at.isoformat(),
            "updated_at": result["user"].updated_at.isoformat()
        }
        return {"user": user_dict, "token": result["token"]}
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/signin", response_model=AuthResponse)
def signin(data: SigninRequest, session: Session = Depends(get_session)):
    try:
        result = auth.signin(session, data.email, data.password)
        # Convert user object to dict for serialization
        user_dict = {
            "id": result["user"].id,
            "email": result["user"].email,
            "name": result["user"].name,
            "created_at": result["user"].created_at.isoformat(),
            "updated_at": result["user"].updated_at.isoformat()
        }
        return {"user": user_dict, "token": result["token"]}
    except ValueError as e:
        raise HTTPException(401, str(e))