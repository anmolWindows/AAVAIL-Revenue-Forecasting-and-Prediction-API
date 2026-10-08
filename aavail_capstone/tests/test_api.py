from app.api import app

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_metrics():
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "requests" in response.get_json()
