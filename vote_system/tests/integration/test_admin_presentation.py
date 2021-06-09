from base64 import b64encode

import pytest
from flask_jwt_extended import create_access_token

from presentation.app import app


credentials = b64encode(b"test_user:test_password").decode("utf-8")


def get_admin_headers(token):
    return {
        "x-access-token": {"userType": "admin"},
        "Authorization": f"Bearer {token}",
    }


VOTER_HEADERS = {"x-access-token": {"userType": "voter"}}


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


def test_create_vote(client):
    response = client.post(
        "vote", headers=VOTER_HEADERS, json={"vote": [3, 4, 5, 1, 5]}
    )
    assert response.status_code == 200


def test_create_candidate(client):
    response = client.post(
        "candidate", headers=ADMIN_HEADERS, json={"username", "random candidate"}
    )
    assert response.status_code == 200


def test_create_election(client):
    response = client.post(
        "election", headers=ADMIN_HEADERS, json={"electionName": "city council 2021"}
    )
    assert response.status_code == 200
