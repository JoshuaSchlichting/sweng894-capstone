from presentation.app import app

import pytest


ADMIN_HEADERS = {"x-access-token": {"userType": "admin"}}
VOTER_HEADERS = {"x-access-token": {"userType": "voter"}}


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_create_user(client):
    response = client.post("user", headers=ADMIN_HEADERS, json={"username": "newuser"})
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
