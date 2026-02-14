#!/usr/bin/env python3
"""
Test script to verify password hash format and verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.auth import verify_password, get_password_hash

def test_password_verification():
    """Test password hashing and verification with known values"""
    
    # Test with a simple password
    test_password = "test1234"
    print(f"Testing with password: '{test_password}'")
    print(f"Password length: {len(test_password)} chars, {len(test_password.encode('utf-8'))} bytes")
    
    # Hash the password
    try:
        hashed = get_password_hash(test_password)
        print(f"Hash created: {hashed[:50]}...")
        print(f"Full hash length: {len(hashed)}")
    except Exception as e:
        print(f"Error hashing password: {e}")
        return
    
    # Verify the correct password
    try:
        result_correct = verify_password(test_password, hashed)
        print(f"Correct password verification: {result_correct}")
    except Exception as e:
        print(f"Error verifying correct password: {e}")
    
    # Verify an incorrect password
    try:
        result_incorrect = verify_password("wrong_password", hashed)
        print(f"Incorrect password verification: {result_incorrect}")
    except Exception as e:
        print(f"Error verifying incorrect password: {e}")
    
    # Test with a longer password (near 72-byte limit)
    long_password = "a" * 70 + "bc"  # 72 characters
    print(f"\nTesting with long password: {len(long_password)} chars, {len(long_password.encode('utf-8'))} bytes")
    
    try:
        long_hashed = get_password_hash(long_password)
        print(f"Long password hash: {long_hashed[:50]}...")
        
        result_long = verify_password(long_password, long_hashed)
        print(f"Long password verification: {result_long}")
        
        # Test with slightly different long password
        result_different = verify_password("a" * 70 + "bd", long_hashed)
        print(f"Different long password verification: {result_different}")
    except Exception as e:
        print(f"Error with long password: {e}")

if __name__ == "__main__":
    test_password_verification()