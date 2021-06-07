from presentation.app import app

import pytest


ADMIN_HEADERS = {
    "x-access-token": {
        "userType": "admin"
    }
}

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_create_user(client):
    response = client.post("user", headers=ADMIN_HEADERS)
    assert response.status_code == 200


def test_create_vote(client):
    response = client.post("vote", headers=ADMIN_HEADERS)
    assert response.status_code == 200


def test_create_candidate(client):
    response = client.post("candidate", headers=ADMIN_HEADERS)
    assert response.status_code == 200


def test_create_election(client):
    response = client.post("election", headers=ADMIN_HEADERS)
    assert response.status_code == 200
