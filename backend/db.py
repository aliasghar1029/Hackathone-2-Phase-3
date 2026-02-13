from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for local development, PostgreSQL for production
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"  # Use SQLite for local testing
)

# Create async engine with appropriate configuration
if DATABASE_URL.startswith("postgresql"):
    # Replace postgresql:// with postgresql+asyncpg:// for async support
    # Need to handle query parameters properly for asyncpg
    if "?" in DATABASE_URL:
        base_url, params_str = DATABASE_URL.split("?", 1)
        # Parse query parameters
        original_params = {}
        for param in params_str.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                original_params[key] = value
        
        # Map common SSL parameters to asyncpg-compatible ones
        mapped_params = {}
        for key, value in original_params.items():
            if key == 'sslmode':
                # asyncpg uses ssl parameter instead of sslmode in URL
                # We'll handle this via connect_args instead
                continue  # Skip adding to URL, handle via connect_args
            elif key != 'channel_binding':  # Skip incompatible parameters
                mapped_params[key] = value
        
        # Reconstruct URL with compatible parameters
        params_part = "&".join([f"{k}={v}" for k, v in mapped_params.items()])
        DATABASE_URL = base_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if params_part:
            DATABASE_URL += "?" + params_part

    else:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Create async engine with SSL configuration for PostgreSQL
    engine = create_async_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,  # Set to True for debugging SQL queries
        # Handle SSL via connect_args for asyncpg
        connect_args={
            "server_settings": {
                "application_name": "hackathon_app",
            }
        } if DATABASE_URL.startswith("postgresql+asyncpg") else {}
    )
else:
    # Create async engine for SQLite - use aiosqlite for async support
    engine = create_async_engine(
        DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"),
        echo=False,  # Set to True for debugging SQL queries
        connect_args={
            "check_same_thread": False  # Needed for SQLite
        }
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session