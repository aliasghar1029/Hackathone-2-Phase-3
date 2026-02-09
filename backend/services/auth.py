# [Task]: T-006
# [From]: speckit.plan §2.2

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlmodel import Session, select
from ..models import User
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def signup(session: Session, email: str, name: str, password: str) -> dict:
    # Check if user exists
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        raise ValueError("Email already registered")

    # Create user
    user = User(
        email=email,
        name=name,
        password_hash=hash_password(password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate token
    token = create_access_token({"user_id": user.id, "email": user.email})
    return {"user": user, "token": token}

def signin(session: Session, email: str, password: str) -> dict:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    token = create_access_token({"user_id": user.id, "email": user.email})
    return {"user": user, "token": token}