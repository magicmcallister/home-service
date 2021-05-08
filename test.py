from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_get_index():
    response = client.get("/")
    assert response.status_code == 200
