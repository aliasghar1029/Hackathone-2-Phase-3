import subprocess
import time
import requests
import threading

def run_server():
    """Run the uvicorn server in a subprocess"""
    subprocess.run([
        "python", "-m", "uvicorn", "main:app", 
        "--host", "127.0.0.1", 
        "--port", "8001",
        "--reload"
    ])

def test_server():
    """Test the server endpoints"""
    time.sleep(3)  # Wait for server to start
    
    BASE_URL = "http://127.0.0.1:8001"
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error during health check: {e}")

    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error during root endpoint test: {e}")

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Test the server
    test_server()