import pytest
from loguru import logger

from core.abstract_data_access_layer import AbstractDataAccessLayer
from core.api_factory import ApiFactory
from core.admin_api import AdminApi
from core.models import User
from core.models import Candidate
from core.models import Election


MOCK_NEW_USER_ID = 1
MOCK_NEW_ELECTION_ID = 1
MOCK_NEW_CANDIDATE_ID = 50


@pytest.fixture
def api(mocker):
    dal = mocker.Mock(spec=AbstractDataAccessLayer)
    dal.create_user.return_value = MOCK_NEW_USER_ID
    dal.create_election.return_value = MOCK_NEW_ELECTION_ID
    dal.create_candidate.return_value = MOCK_NEW_CANDIDATE_ID

    api_factory = ApiFactory(token={}, data_access_layer=dal, logger=logger)
    return api_factory.create_admin_api()


def test_create_user(api):
    # act
    new_user_id = api.create_user("Test User")

    # assert
    assert new_user_id == MOCK_NEW_USER_ID


def test_create_candidate(api):
    # act
    candidate_id = api.create_candidate(username="some candidate")

    # assert
    assert candidate_id == MOCK_NEW_CANDIDATE_ID


def test_create_election(api):
    # act
    election_id = api.create_election(election_name="City Council Election")

    # assert
    assert election_id == MOCK_NEW_ELECTION_ID
