#!/usr/bin/env python3
"""
Simple test script to verify password hashing and verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth import get_password_hash, verify_password

def test_password_functions():
    """Test password hashing and verification functions"""
    
    # Test passwords of different lengths
    test_passwords = [
        "short123",  # Short password
        "medium_password_123",  # Medium password
        "very_long_password_that_might_be_over_the_72_byte_limit_for_bcrypt_verification",  # Long password
        "password_with_special_chars!@#$%^&*()",  # Password with special chars
        "password_with_unicode_üñíçødé",  # Password with unicode
    ]
    
    print("Testing password hashing and verification:")
    print("=" * 50)
    
    for i, password in enumerate(test_passwords, 1):
        print(f"\nTest {i}: '{password}'")
        print(f"  Length: {len(password)} characters, {len(password.encode('utf-8'))} bytes")
        
        try:
            # Hash the password
            hashed = get_password_hash(password)
            print(f"  Hash created successfully: {hashed[:30]}...")
            
            # Verify the password
            is_valid = verify_password(password, hashed)
            print(f"  Verification result: {is_valid}")
            
            # Test with wrong password
            wrong_password_valid = verify_password("wrong_password", hashed)
            print(f"  Wrong password verification: {wrong_password_valid}")
            
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_password_functions()