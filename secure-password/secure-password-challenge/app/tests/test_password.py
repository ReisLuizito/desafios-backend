from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_password_returns_204():
    payload = {"password": "vYQIYx0&p$yfI^r"}
    r = client.post("/validate-password", json=payload)
    assert r.status_code == 204

def test_too_short_and_missing_many_rules_returns_400_with_list():
    payload = {"password": "abczxyy"}
    r = client.post("/validate-password", json=payload)
    assert r.status_code == 400
    detail = r.json()["detail"]
    codes = {err["code"] for err in detail}
    assert "length" in codes
    assert "uppercase" in codes
    assert "digit" in codes
    assert "special" in codes

def test_missing_uppercase_only():
    payload = {"password": "abc123!@#x"}
    r = client.post("/validate-password", json=payload)
    assert r.status_code == 400
    detail = r.json()["detail"]
    assert any(err["code"] == "uppercase" for err in detail)

def test_missing_lowercase_only():
    payload = {"password": "ABC123!@#X"}
    r = client.post("/validate-password", json=payload)
    assert r.status_code == 400
    detail = r.json()["detail"]
    assert any(err["code"] == "lowercase" for err in detail)

def test_missing_digit_only():
    payload = {"password": "Abcdef!@"}
    r = client.post("/validate-password", json=payload)
    assert r.status_code == 400
    assert any(err["code"] == "digit" for err in r.json()["detail"])

def test_missing_special_only():
    payload = {"password": "Abcdef12"}
    r = client.post("/validate-password", json=payload)
    assert r.status_code == 400
    assert any(err["code"] == "special" for err in r.json()["detail"])
