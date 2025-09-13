from fastapi.testclient import TestClient
from app.main import app
from app.db import engine
from sqlalchemy import text

client = TestClient(app)

def seed_example_data():
    data = [
        {"name":"Lanchonete","x":27,"y":12},
        {"name":"Posto","x":31,"y":18},
        {"name":"Joalheria","x":15,"y":12},
        {"name":"Floricultura","x":19,"y":21},
        {"name":"Pub","x":12,"y":8},
        {"name":"Supermercado","x":23,"y":6},
        {"name":"Churrascaria","x":28,"y":2},
    ]
    for d in data:
        r = client.post("/pois", json=d)
        assert r.status_code == 201

def reset_db():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM pois"))
        conn.commit()

def test_create_and_list_pois():
    reset_db()
    r = client.post("/pois", json={"name":"POI A","x":10,"y":20})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "POI A"
    assert data["x"] == 10 and data["y"] == 20

    r2 = client.get("/pois")
    assert r2.status_code == 200
    items = r2.json()
    assert any(p["name"] == "POI A" for p in items)

def test_nearby_matches_example_from_prompt():
    reset_db()
    seed_example_data()
    r = client.get("/pois/nearby", params={"x":20,"y":10,"max_distance":10})
    assert r.status_code == 200
    names = [p["name"] for p in r.json()]
    for expected in ["Lanchonete","Joalheria","Pub","Supermercado"]:
        assert expected in names
    for not_expected in ["Posto","Floricultura","Churrascaria"]:
        assert not_expected not in names

def test_validation_non_negative_coords():
    reset_db()
    r = client.post("/pois", json={"name":"X","x":-1,"y":0})
    assert r.status_code == 422
    r = client.get("/pois/nearby", params={"x":-1,"y":0,"max_distance":10})
    assert r.status_code == 422

def test_max_distance_must_be_positive():
    reset_db()
    r = client.get("/pois/nearby", params={"x":0,"y":0,"max_distance":0})
    assert r.status_code == 422
