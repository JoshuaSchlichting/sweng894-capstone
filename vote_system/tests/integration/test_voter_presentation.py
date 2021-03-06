import pytest
from loguru import logger

from presentation.app import app


@pytest.fixture
def data_access_layer():
    from mongomock import MongoClient

    # from pymongo import MongoClient
    import db_implementation

    db = db_implementation.MongoDbApi(MongoClient(), logger=logger)
    db.create_user(
        username="test", password="test", user_type="admin", is_candidate=True
    )
    return db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def token(client, mocker, monkeypatch, data_access_layer):
    dal = mocker.Mock()
    dal.return_value = data_access_layer
    monkeypatch.setattr("presentation.app._get_data_access_layer", dal)
    response = client.post(
        "/login", data=dict(inputUsername="test", inputPassword="test")
    )
    token = response.json["access_token"]
    return token


def get_voter_headers(token):
    return {
        "Authorization": f"Bearer {token}",
    }


def test_create_vote(client, token):
    response = client.post(
        "/vote",
        headers=get_voter_headers(token),
        json={"rankedCandidateList": [3, 4, 5, 1, 5], "electionId": 4, "userId": 444},
    )
    assert response.status_code == 200
