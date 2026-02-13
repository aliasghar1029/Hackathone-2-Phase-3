import requests
import time

def test_bcrypt_fix():
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Test signup with a long password
    url = "http://127.0.0.1:8001/api/auth/signup"
    
    # Test with a password that's too long (should be rejected)
    long_password_user = {
        "name": "Test User Long Password",
        "email": "testlong@example.com",
        "password": "a" * 73  # 73 characters, exceeding the 72-byte limit
    }

    print("Testing signup with password that exceeds 72 bytes...")
    try:
        response = requests.post(url, json=long_password_user)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ SUCCESS: Long password properly rejected")
        else:
            print("❌ FAILURE: Long password was not properly rejected")
    except Exception as e:
        print(f"Error during test: {e}")
    
    # Test with a valid password
    valid_user = {
        "name": "Valid Test User",
        "email": "valid@example.com",
        "password": "validpassword123"
    }
    
    print("\nTesting signup with valid credentials...")
    try:
        response = requests.post(url, json=valid_user)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS: Valid signup works correctly")
        else:
            print(f"Response: {response.text}")
            print("❌ FAILURE: Valid signup failed")
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_bcrypt_fix()