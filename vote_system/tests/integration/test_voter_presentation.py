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


def get_voter_headers(token):
    return {
        "x-access-token": {"userType": "voter"},
        "Authorization": f"Bearer {token}",
    }


def test_create_vote(client, token):
    response = client.post(
        "/vote",
        headers=get_voter_headers(token),
        json={"rankedCandidateList": [3, 4, 5, 1, 5], "electionId": 4, "userId": 444},
    )
    assert response.status_code == 200
