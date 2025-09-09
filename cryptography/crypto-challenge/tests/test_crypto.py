from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
from app.db import engine

client = TestClient(app)

def test_create_and_read_payment_transparent_crypto():
    payload = {
        "userDocument": "36140781833",
        "creditCardToken": "abc123",
        "value": 5999
    }
    r = client.post("/payments", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    pid = data["id"]
    # API devolve plaintext (decriptado)
    assert data["userDocument"] == "36140781833"
    assert data["creditCardToken"] == "abc123"
    assert data["value"] == 5999

    # No banco, os campos devem estar encriptados (não iguais ao plaintext)
    with engine.connect() as conn:
        row = conn.execute(text("SELECT userDocument, creditCardToken FROM payments WHERE id=:id"), {"id": pid}).fetchone()
        assert row is not None
        enc_doc, enc_token = row
        assert enc_doc != "36140781833"
        assert enc_token != "abc123"
        # Devem parecer base64 (caracteres seguros e tamanho maior que o plaintext)
        assert isinstance(enc_doc, str) and len(enc_doc) > len("36140781833")
        assert isinstance(enc_token, str) and len(enc_token) > len("abc123")

def test_update_and_delete_payment():
    # cria
    r = client.post("/payments", json={
        "userDocument": "11122233344",
        "creditCardToken": "xyz456",
        "value": 1000
    })
    assert r.status_code == 201
    pid = r.json()["id"]

    # update parcial
    r2 = client.patch(f"/payments/{pid}", json={"value": 1500})
    assert r2.status_code == 200
    assert r2.json()["value"] == 1500

    # delete
    r3 = client.delete(f"/payments/{pid}")
    assert r3.status_code == 204

    # not found depois do delete
    r4 = client.get(f"/payments/{pid}")
    assert r4.status_code == 404
