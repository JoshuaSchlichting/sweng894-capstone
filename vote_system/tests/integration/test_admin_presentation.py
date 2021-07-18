import pytest
from loguru import logger

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
def data_access_layer():
    from mongomock import MongoClient
    # from pymongo import MongoClient
    import db_implementation

    db = db_implementation.MongoDbApi(MongoClient(), logger=logger)
    db.create_user(
        username="test",
        password="test",
        is_candidate=False,
        user_type="admin"
    )
    return db


@pytest.fixture
def token(client):
    response = client.post(
        "/login", data=dict(inputUsername="test", inputPassword="test")
    )
    if response.status_code != 200:
        raise Exception(f"STATUS CODE {response.status_code}")
    token = response.json["access_token"]
    return token

@pytest.fixture(autouse=True)
def patch_data_access_layer(monkeypatch, mocker, data_access_layer):
    dal = mocker.Mock()
    dal.return_value = data_access_layer
    monkeypatch.setattr("presentation.app._get_data_access_layer", dal)


def test_create_user(client, token):

    response = client.post(
        "/user",
        headers=get_admin_headers(token),
        json={"username": "new admin", "userType": "admin", "isCandidate": "true"},
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
        json={
            "electionName": "city council 2021",
            "startDate": "2021-01-01",
            "endDate": "2021-01-01",
        },
    )
    assert response.status_code == 200


def test_add_candidate_to_election(
    client, token, data_access_layer,
):
    election_id = data_access_layer.create_election("city council 2021", "2021-01-01", "2021-02-01")

    response = client.post(
        "election/candidate",
        headers=get_admin_headers(token),
        json={"candidateId": "60eba2ff9615f8d85509b34f", "electionId": election_id},
    )

    assert response.status_code == 200
