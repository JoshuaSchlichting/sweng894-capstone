import pytest

from presentation.app import app


def get_admin_headers(token):
    return {
        "x-access-token": {"userType": "admin"},
        "Authorization": f"Bearer {token}",
    }


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


def test_create_user(client, token):
    response = client.post(
        "/user", headers=get_admin_headers(token), json={"username": "newuser"}
    )
    assert response.status_code == 200


def test_create_candidate(client, token):
    response = client.post(
        "/candidate",
        headers=get_admin_headers(token),
        json={"username": "random candidate"},
    )
    assert response.status_code == 200


def test_create_election(client, token):
    response = client.post(
        "/election",
        headers=get_admin_headers(token),
        json={"electionName": "city council 2021"},
    )
    assert response.status_code == 200
