import pytest

from presentation.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def token(client):
    response = client.post(
        "/login", data=dict(inputUsername="test", inputPassword="test")
    )
    if response.status_code != 200:
        raise Exception(f"STATUS CODE {response.status_code}")
    token = response.json["access_token"]
    return token


def test_index_loads(client):
    response = client.get("/")
    assert response.data.endswith(b"html>")
    assert response.status_code == 200
