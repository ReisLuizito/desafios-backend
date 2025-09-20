from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
from app.db import engine
from app.config import settings
from app import services
import json

client = TestClient(app)

def reset_db():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM transfers"))
        conn.commit()

def signed_headers(body: dict, idem_key: str):
    raw = json.dumps(body, separators=(",", ":")).encode("utf-8")
    sig = services.body_signature(settings.SIGNING_SECRET, raw)
    return {
        "Content-Type": "application/json",
        "X-Idempotency-Key": idem_key,
        "X-Signature": sig,
    }, raw

def test_create_transfer_first_time_201():
    reset_db()
    body = {"amount": 12345, "currency": "BRL", "beneficiary_account": "001-1234-5"}
    headers, _ = signed_headers(body, idem_key="abc-1")
    r = client.post("/transfers", json=body, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["amount"] == 12345
    assert data["currency"] == "BRL"
    assert data["beneficiary_account"] == "001-1234-5"
    assert "id" in data

def test_idempotent_same_payload_200_same_id():
    reset_db()
    body = {"amount": 500, "currency": "BRL", "beneficiary_account": "002-9999-0"}
    headers, _ = signed_headers(body, idem_key="same-key")
    r1 = client.post("/transfers", json=body, headers=headers)
    assert r1.status_code == 201
    id1 = r1.json()["id"]

    r2 = client.post("/transfers", json=body, headers=headers)
    assert r2.status_code == 200
    id2 = r2.json()["id"]
    assert id1 == id2

def test_idempotent_conflict_409():
    reset_db()
    body1 = {"amount": 100, "currency": "BRL", "beneficiary_account": "003-7"}
    headers1, _ = signed_headers(body1, idem_key="K-1")
    r1 = client.post("/transfers", json=body1, headers=headers1)
    assert r1.status_code == 201

    body2 = {"amount": 200, "currency": "BRL", "beneficiary_account": "003-7"}  # altera amount
    headers2, _ = signed_headers(body2, idem_key="K-1")
    r2 = client.post("/transfers", json=body2, headers=headers2)
    assert r2.status_code == 409

def test_missing_signature_401():
    reset_db()
    body = {"amount": 10, "currency": "USD", "beneficiary_account": "XYZ"}
    r = client.post("/transfers", json=body, headers={"X-Idempotency-Key": "no-sig"})
    assert r.status_code == 401

def test_missing_idem_key_400():
    reset_db()
    body = {"amount": 10, "currency": "USD", "beneficiary_account": "XYZ"}
    raw = json.dumps(body, separators=(",", ":")).encode("utf-8")
    sig = services.body_signature(settings.SIGNING_SECRET, raw)
    r = client.post("/transfers", json=body, headers={"X-Signature": sig})
    assert r.status_code == 400

def test_get_by_id_404_and_200():
    reset_db()
    r404 = client.get("/transfers/999999")
    assert r404.status_code == 404

    body = {"amount": 6400, "currency": "EUR", "beneficiary_account": "ABC-123"}
    headers, _ = signed_headers(body, idem_key="kkk-9")
    r = client.post("/transfers", json=body, headers=headers)
    tid = r.json()["id"]

    r2 = client.get(f"/transfers/{tid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == tid