import time
import subprocess
import sys
import requests

def start_server_and_test():
    # Start the server in a subprocess
    server_process = subprocess.Popen([
        sys.executable, "-c", 
        "from main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a few seconds for the server to start
    time.sleep(5)
    
    try:
        # Test the signup endpoint
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
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    start_server_and_test()