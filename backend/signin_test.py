import time
import subprocess
import sys
import requests

def test_signin():
    # Start the server in a subprocess
    server_process = subprocess.Popen([
        sys.executable, "-c", 
        "from main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a few seconds for the server to start
    time.sleep(5)
    
    try:
        # First, signup a user
        signup_url = "http://127.0.0.1:8000/api/auth/signup"
        user_data = {
            "name": "Test User Signin",
            "email": "signin@test.com",
            "password": "validpassword123"
        }
        
        print("Creating user for signin test...")
        signup_response = requests.post(signup_url, json=user_data)
        print(f"Signup Status: {signup_response.status_code}")
        
        # Now test signin with correct credentials
        signin_url = "http://127.0.0.1:8000/api/auth/signin"
        signin_data = {
            "email": "signin@test.com",
            "password": "validpassword123"
        }
        
        print("\nTesting signin with correct credentials...")
        signin_response = requests.post(signin_url, json=signin_data)
        print(f"Signin Status: {signin_response.status_code}")
        print(f"Signin Response: {signin_response.text}")
        
        # Test signin with wrong password
        signin_wrong_data = {
            "email": "signin@test.com",
            "password": "wrongpassword"
        }
        
        print("\nTesting signin with wrong password...")
        signin_wrong_response = requests.post(signin_url, json=signin_wrong_data)
        print(f"Wrong Signin Status: {signin_wrong_response.status_code}")
        print(f"Wrong Signin Response: {signin_wrong_response.text}")
        
        # Test signin with a very long password (should be handled gracefully)
        signin_long_data = {
            "email": "signin@test.com",
            "password": "a" * 80  # Very long password
        }
        
        print("\nTesting signin with very long password...")
        signin_long_response = requests.post(signin_url, json=signin_long_data)
        print(f"Long Password Signin Status: {signin_long_response.status_code}")
        print(f"Long Password Signin Response: {signin_long_response.text}")
        
        print("\nSignin tests completed!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_signin()