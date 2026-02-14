#!/usr/bin/env python3
"""
Debug script for authentication issues
"""

import asyncio
from sqlmodel import select
from Backend.db import get_session, engine
from Backend.models import User
from Backend.services.auth import verify_password
from Backend.main import lifespan
from contextlib import asynccontextmanager

async def debug_authentication():
    """Debug authentication by checking a specific user's password hash"""
    
    # Create async context manager for the lifespan
    @asynccontextmanager
    async def app_lifespan(app):
        async with lifespan(app) as state:
            yield state
    
    # Mock app for lifespan
    class MockApp:
        pass
    
    mock_app = MockApp()
    
    async with app_lifespan(mock_app):
        async with get_session(engine) as session:
            # Query for the specific user
            email = "aliasgharboy514@gmail.com"
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                print(f"User with email {email} not found in database")
                return
            
            print(f"User found: {user.name}")
            print(f"User ID: {user.id}")
            print(f"Password hash: {user.password_hash[:50]}...")  # Show first 50 chars
            print(f"Hash length: {len(user.password_hash)}")
            
            # Test password verification with a sample password
            test_passwords = [
                "your_actual_password_here",  # Replace with the actual password
                "test1234",  # Common test password
                "",  # Empty password
            ]
            
            for test_pass in test_passwords:
                if test_pass == "your_actual_password_here":
                    continue  # Skip placeholder
                    
                try:
                    is_valid = verify_password(test_pass, user.password_hash)
                    print(f"Password '{test_pass}' verification: {is_valid}")
                except Exception as e:
                    print(f"Error verifying password '{test_pass}': {e}")

if __name__ == "__main__":
    asyncio.run(debug_authentication())