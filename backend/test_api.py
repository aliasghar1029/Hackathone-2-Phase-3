# [Task]: T-033
# [From]: speckit.plan §10

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to TODO AI Chatbot API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "todo-ai-chatbot-api"}

# Additional tests would go here once routes are fully implemented