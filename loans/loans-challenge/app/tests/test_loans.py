from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_customer_high_income():
    payload = {"age": 40, "cpf": "111.111.111-11", "name": "Alice", "income": 7000, "location": "RJ"}
    r = client.post("/customer-loans", json=payload)
    data = r.json()
    assert r.status_code == 200
    assert data["customer"] == "Alice"
    assert {"type": "CONSIGNMENT", "interest_rate": 2} in data["loans"]
    assert len(data["loans"]) == 1

def test_customer_low_income():
    payload = {"age": 25, "cpf": "222.222.222-22", "name": "Bob", "income": 2500, "location": "SP"}
    r = client.post("/customer-loans", json=payload)
    data = r.json()
    assert r.status_code == 200
    types = {loan["type"] for loan in data["loans"]}
    assert "PERSONAL" in types
    assert "GUARANTEED" in types
    assert len(data["loans"]) == 2

def test_customer_middle_income_young_sp():
    payload = {"age": 26, "cpf": "333.333.333-33", "name": "Carol", "income": 4000, "location": "SP"}
    r = client.post("/customer-loans", json=payload)
    data = r.json()
    assert r.status_code == 200
    types = {loan["type"] for loan in data["loans"]}
    assert "PERSONAL" in types
    assert "GUARANTEED" in types
    assert "CONSIGNMENT" not in types

def test_customer_middle_income_old_rj():
    payload = {"age": 35, "cpf": "444.444.444-44", "name": "Dan", "income": 4000, "location": "RJ"}
    r = client.post("/customer-loans", json=payload)
    data = r.json()
    assert r.status_code == 200
    assert data["loans"] == []
