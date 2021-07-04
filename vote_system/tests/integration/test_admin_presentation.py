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
def data_access_layer():
    from mongomock import MongoClient
    import db_implementation
    db = db_implementation.MongoDbApi(MongoClient())
    db.create_user('test', 'test')
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


def test_create_user(client, token, data_access_layer, monkeypatch, mocker):
    dal = mocker.Mock()
    dal.return_value = data_access_layer
    monkeypatch.setattr('presentation.app._get_data_access_layer', dal)
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
