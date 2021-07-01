
import pytest
from mongomock import MongoClient
from loguru import logger

from core.dal import create_mongo_api



pytest.fixture
def sud():
    """System Under Test (SUD), which is the data access layer for mongo DB"""
    return create_mongo_api(MongoClient())


def test_cast_vote(sud):

    # arrange
    user_id = 1569568
    election_id = 14432
    ranked_candidate_list = [51235, 552346, 6123, 4123, 41234]

    # act
    new_vote_id = sud.cast_vote(
        user_id=user_id,
        election_id=election_id,
        ranked_candidate_list=ranked_candidate_list
    )

    new_vote_data = sud.get_vote(new_vote_id)

    # assert
    assert new_vote_data["user_id"] == user_id
    assert new_vote_data["election_id"] == election_id
    assert new_vote_data["ranked_candidate_list"] == ranked_candidate_list


def test_create_candidate_from_non_existing_user(sud):
    user_id = sud.create_candidate("John Doe")
    assert type(user_id) is int


def test_create_candidate_from_existing_user(sud):

    username = "John Doe"

    # arrange
    user_id = sud.create_user(username=username, password="pass")

    # convert this user into a candidate
    candidate_id = sud.create_candidate(username)

    # act
    assert candidate_id == user_id


def test_create_user(sud):
    username = "test user"
    user_id = sud.create_user(username)
    user_info = sud.get_user_info_by_name(username)
    assert user_info["id"] == user_id


def test_create_election(sud):

    # arrange
    ranked_candidate_list = [51235, 552346, 6123, 4123, 41234]

    # act
    election_id = sud.create_election("city council", ranked_candidate_list) 
    election = sud.get_election(election_id)

    # assert
    assert election["ranked_candidate_list"] == ranked_candidate_list
    assert type(election_id) is int


def test_get_user_is_valid(sud):
    assert sud.get_user_is_valid(username="test", password="testpassword") is True

def test_create_password(username, password)