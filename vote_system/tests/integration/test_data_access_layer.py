import pytest
from mongomock import MongoClient
from loguru import logger

from db_implementation import MongoDbApi, create_mongo_api


@pytest.fixture
def sud() -> MongoDbApi:
    """System Under Test (SUD), which is the data access layer for mongo DB"""
    return MongoDbApi(MongoClient(), logger=logger)


def test_cast_vote(sud):

    # arrange
    user_id = 1569568
    election_id = 14432
    ranked_candidate_list = [51235, 552346, 6123, 4123, 41234]

    # act
    new_vote_id = sud.cast_vote(
        user_id=user_id,
        election_id=election_id,
        ranked_candidate_list=ranked_candidate_list,
    )

    new_vote_data = sud.get_vote(new_vote_id)

    # assert
    assert new_vote_data["user_id"] == user_id
    assert new_vote_data["election_id"] == election_id
    assert new_vote_data["ranked_candidate_list"] == ranked_candidate_list


def test_create_candidate_from_non_existing_user(sud):
    user_id = sud.create_candidate("John Doe")
    assert type(user_id) is str


def test_create_candidate_from_existing_user(sud):

    username = "John Doe"

    # arrange
    user_id = sud.create_user(username=username, password="pass", user_type="standard", is_candidate=False)

    # convert this user into a candidate
    candidate_id = sud.create_candidate(username)

    # act
    assert candidate_id == user_id


def test_create_user(sud):
    username = "test user"
    user_id = sud.create_user(username=username, user_type="standard", is_candidate=True)
    user_info = sud.get_user_info_by_name(username)
    assert str(user_info["id"]) == user_id


def test_create_election(sud):

    # act
    election_id = sud.create_election("city council", "2021-01-01", "2021-02-02")
    election = sud.get_election(election_id)

    # assert
    assert type(election_id) is str


def test_get_user_is_valid(sud):
    assert sud.get_user_is_valid(username="test", password="testpassword") is False
    sud.create_user(username="test", password="testpassword", user_type="standard", is_candidate=True)
    assert sud.get_user_is_valid(username="test", password="testpassword") is True
