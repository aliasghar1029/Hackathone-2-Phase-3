import requests
import time

def test_server():
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Test the health endpoint first
    health_url = "http://127.0.0.1:8002/health"
    print("Testing health endpoint...")
    try:
        response = requests.get(health_url)
        print(f"Health check - Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test signup with a long password
    signup_url = "http://127.0.0.1:8002/api/auth/signup"
    
    # Test with a password that's too long (should be rejected)
    long_password_user = {
        "name": "Test User Long Password",
        "email": "testlong@example.com",
        "password": "a" * 73  # 73 characters, exceeding the 72-byte limit
    }

    print("\nTesting signup with password that exceeds 72 bytes...")
    try:
        response = requests.post(signup_url, json=long_password_user)
        print(f"Long password - Status Code: {response.status_code}")
        print(f"Long password - Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ SUCCESS: Long password properly rejected")
        else:
            print("❌ FAILURE: Long password was not properly rejected")
    except Exception as e:
        print(f"Error during long password test: {e}")
    
    # Test with a valid password
    valid_user = {
        "name": "Valid Test User",
        "email": "valid@example.com",
        "password": "validpassword123"
    }
    
    print("\nTesting signup with valid credentials...")
    try:
        response = requests.post(signup_url, json=valid_user)
        print(f"Valid signup - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS: Valid signup works correctly")
        else:
            print(f"Valid signup - Response: {response.text}")
            print("❌ FAILURE: Valid signup failed")
    except Exception as e:
        print(f"Error during valid signup test: {e}")

if __name__ == "__main__":
    test_server()