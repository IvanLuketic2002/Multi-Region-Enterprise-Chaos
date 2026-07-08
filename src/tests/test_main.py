from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Trenutna regija" in response.json()["message"]

def test_health_check_clean():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_health_check_fail_simulation():
    response_toggle = client.post("/toggle-health")
    assert response_toggle.status_code == 200
    
    response_health = client.get("/health")
    assert response_health.status_code == 500
    
    client.post("/toggle-health")
