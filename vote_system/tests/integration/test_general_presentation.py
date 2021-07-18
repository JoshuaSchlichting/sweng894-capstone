import pytest
from loguru import logger

from presentation.app import app


@pytest.fixture
def data_access_layer():
    from mongomock import MongoClient
    # from pymongo import MongoClient
    import db_implementation

    db = db_implementation.MongoDbApi(MongoClient(), logger=logger)
    db.create_user(username="test", password="test", is_candidate=True, user_type="admin")
    return db


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


def test_get_election_returns_election(client, mocker, monkeypatch, data_access_layer):
    dal = mocker.Mock()
    dal.return_value = data_access_layer
    monkeypatch.setattr("presentation.app._get_data_access_layer", dal)
    election_id = dal().create_election("city council 2021", "2021-01-01", "2021-02-02")
    response = client.get("/election", json={"electionId": election_id})
    assert response.status_code == 200


def test_get_all_elections_returns_elections(
    client, mocker, monkeypatch, data_access_layer
):
    dal = mocker.Mock()
    dal.return_value = data_access_layer
    monkeypatch.setattr("presentation.app._get_data_access_layer", dal)
    dal().create_election("test name1", "2022-01-01", "2022-02-02")
    dal().create_election("test name2", "2022-01-01", "2022-02-02")
    elections = dal().get_all_elections()
    response = client.get("/election/all")
    assert response.status_code == 200
