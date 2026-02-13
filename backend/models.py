from sqlmodel import SQLModel, Field, create_engine, Column
from sqlalchemy import DateTime
from typing import Optional
from datetime import datetime
import uuid
from pydantic import BaseModel, Field as PydanticField


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str


class User(UserBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    user: UserRead
    token: str


class TaskBase(SQLModel):
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)


class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskRead(TaskBase):
    id: int
    user_id: str
    created_at: str
    updated_at: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskToggleComplete(SQLModel):
    completed: bool


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="user.id")
    role: str  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)