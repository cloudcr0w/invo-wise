import sys, pathlib
# sets pythonpath to repo root
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from api.main import app  # services/api/main.py as module for main.py

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_version():
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert "version" in body and "env" in body
