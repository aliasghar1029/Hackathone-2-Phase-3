import requests
import json

def debug_test():
    url = "http://127.0.0.1:8000/api/auth/signup"
    
    # Test with a very simple password
    test_user = {
        "name": "Debug User",
        "email": "debug@example.com",
        "password": "simple123"
    }
    
    print(f"Password: '{test_user['password']}'")
    print(f"Password length: {len(test_user['password'])}")
    print(f"Password byte length: {len(test_user['password'].encode('utf-8'))}")
    
    response = requests.post(url, json=test_user)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test with exactly 72 bytes
    exactly_72_bytes = "a" * 72
    test_user_72 = {
        "name": "72 Byte User",
        "email": "72bytes@example.com",
        "password": exactly_72_bytes
    }
    
    print(f"\nPassword: '{exactly_72_bytes}'")
    print(f"Password length: {len(exactly_72_bytes)}")
    print(f"Password byte length: {len(exactly_72_bytes.encode('utf-8'))}")
    
    response = requests.post(url, json=test_user_72)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    debug_test()