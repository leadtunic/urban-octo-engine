from fastapi.testclient import TestClient
from run import app

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_time():
    response = client.get("/time")
    assert response.status_code == 200
    assert "current_time" in response.json()

def test_soma():
    response = client.get("/soma?a=2&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 5}

def test_create_item():
    data = {"name": "foo", "value": 42}
    response = client.post("/item", json=data)
    assert response.status_code == 200
    assert "Recebido foo com valor 42" in response.json()["mensagem"]

def test_invert():
    response = client.get("/invert?texto=python")
    assert response.status_code == 200
    assert response.json() == {"invertido": "nohtyp"}
