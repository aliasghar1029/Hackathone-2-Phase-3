# [Task]: T-022
# [From]: speckit.plan §10

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from db import init_db

@pytest.fixture
def client():
    """Test client for the API"""
    with TestClient(app) as test_client:
        yield test_client

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_auth_routes_exist(client):
    """Test that auth routes are registered"""
    # Test that we get proper error for missing data rather than 404
    response = client.post("/api/auth/signup")
    # Should get validation error, not 404
    assert response.status_code in [422, 400]

    response = client.post("/api/auth/signin")
    # Should get validation error, not 404
    assert response.status_code in [422, 400]

if __name__ == "__main__":
    pytest.main([__file__])