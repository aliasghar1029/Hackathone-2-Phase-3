import requests
import json

# Test the signup endpoint
def test_signup():
    url = "http://127.0.0.1:8000/api/auth/signup"
    
    # Test with a valid user
    valid_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "validpassword123"
    }
    
    print("Testing signup with valid credentials...")
    response = requests.post(url, json=valid_user)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test with a password that's too long
    long_password_user = {
        "name": "Test User Long Password",
        "email": "testlong@example.com",
        "password": "a" * 73  # 73 characters, exceeding the 72-byte limit
    }
    
    print("\nTesting signup with password that exceeds 72 bytes...")
    response = requests.post(url, json=long_password_user)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test with a short password
    short_password_user = {
        "name": "Test User Short Password",
        "email": "testshort@example.com",
        "password": "short"
    }
    
    print("\nTesting signup with password that's too short...")
    response = requests.post(url, json=short_password_user)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_signup()