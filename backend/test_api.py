import requests
import json

# Test the API endpoints
BASE_URL = "http://127.0.0.1:8001"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error during health check: {e}")

def test_root():
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error during root endpoint test: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_health()
    test_root()
    print("Tests completed.")