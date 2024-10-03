
import sys
import os

from fastapi.testclient import TestClient
from src.main import app


testing_client = TestClient(app)

def test_health():
    response = testing_client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Service is healthy!"}

