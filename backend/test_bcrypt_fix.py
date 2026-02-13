"""
Test script to verify bcrypt password length fix
"""
from services.auth import get_password_hash, verify_password

def test_short_password():
    """Test a normal short password"""
    password = "shortpass123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) == True
    print("[PASS] Short password test passed")

def test_long_password():
    """Test a password that exceeds 72 bytes"""
    # Create a password longer than 72 bytes
    long_password = "a" * 80  # 80 bytes
    try:
        hashed = get_password_hash(long_password)
        # The password should be automatically truncated and verified
        assert verify_password(long_password, hashed) == True
        print("[PASS] Long password test passed")
    except ValueError as e:
        print(f"[FAIL] Long password test failed: {e}")

def test_unicode_password():
    """Test a password with unicode characters that might exceed 72 bytes when encoded"""
    # Unicode password that might exceed 72 bytes when encoded
    unicode_password = "üñíçødé" * 15  # Multiple unicode chars
    try:
        hashed = get_password_hash(unicode_password)
        # The password should be automatically truncated and verified
        assert verify_password(unicode_password, hashed) == True
        print("[PASS] Unicode password test passed")
    except ValueError as e:
        print(f"[FAIL] Unicode password test failed: {e}")

def test_exact_72_bytes():
    """Test a password that is exactly 72 bytes"""
    # Create a password that is exactly 72 bytes
    exact_password = "a" * 72
    hashed = get_password_hash(exact_password)
    assert verify_password(exact_password, hashed) == True
    print("[PASS] Exactly 72 bytes password test passed")

def test_just_over_72_bytes():
    """Test a password that is just over 72 bytes"""
    # Create a password that is just over 72 bytes
    slightly_over_password = "a" * 75
    try:
        hashed = get_password_hash(slightly_over_password)
        # The password should be automatically truncated and verified
        assert verify_password(slightly_over_password, hashed) == True
        print("[PASS] Just over 72 bytes password test passed")
    except ValueError as e:
        print(f"[FAIL] Just over 72 bytes password test failed: {e}")

if __name__ == "__main__":
    print("Testing bcrypt password length fix...")
    test_short_password()
    test_long_password()
    test_unicode_password()
    test_exact_72_bytes()
    test_just_over_72_bytes()
    print("All tests completed!")