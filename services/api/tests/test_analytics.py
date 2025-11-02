

from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

def test_analytics_basic_response():
    """
    Basic smoke test for /analytics endpoint.
    Ensures the endpoint is reachable and returns valid JSON keys.
    """
    r = client.get("/analytics")
    assert r.status_code == 200
    data = r.json()
    assert "analytics" in data
    assert "ytd" in data
    assert "generated_at" in data
