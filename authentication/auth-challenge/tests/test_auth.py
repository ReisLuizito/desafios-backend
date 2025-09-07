from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_foo_bar_valid_token_plain():
    r = client.get("/foo-bar", headers={"Authorization": settings.AUTH_TOKEN})
    assert r.status_code == 204

def test_foo_bar_valid_token_bearer():
    r = client.get("/foo-bar", headers={"Authorization": f"Bearer {settings.AUTH_TOKEN}"})
    assert r.status_code == 204

def test_foo_bar_invalid_token():
    r = client.get("/foo-bar", headers={"Authorization": "WRONG"})
    assert r.status_code == 401
    assert "inválido" in r.json()["detail"].lower()

def test_foo_bar_missing_token():
    r = client.get("/foo-bar")
    assert r.status_code == 401

def test_health_is_public():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_new_endpoint_is_also_protected():
    r = client.get("/another")
    assert r.status_code == 401

    r2 = client.get("/another", headers={"Authorization": f"Bearer {settings.AUTH_TOKEN}"})
    assert r2.status_code == 200
    assert r2.json() == {"ok": True}
