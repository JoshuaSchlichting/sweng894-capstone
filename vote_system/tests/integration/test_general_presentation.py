import pytest

from presentation.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def token(client):
    response = client.post("/login", json={"username": "test", "password": "test"})
    token = response.json["access_token"]
    return token


def test_index_loads(client):
    response = client.get("/")
    assert response.data == b"SUCCESS"
    assert response.status_code == 200
