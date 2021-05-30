import pytest

from core.abstract_data_access_layer import AbstractDataAccessLayer
from core.api_factory import ApiFactory
from core.admin_api import AdminApi
from core.models import User
from core.models import Candidate
from core.models import Election

import pytest
from loguru import logger

MOCK_NEW_USER_ID = 1
MOCK_NEW_ELECTION_ID = 1
MOCK_NEW_CANDIDATE_ID = 50


@pytest.fixture
def data_access_layer(mocker):
    dal = mocker.Mock(spec=AbstractDataAccessLayer)
    dal.create_user.return_value = MOCK_NEW_USER_ID
    dal.create_election.return_value = MOCK_NEW_ELECTION_ID
    dal.create_candidate.return_value = MOCK_NEW_CANDIDATE_ID
    return dal

def test_create_user(data_access_layer):
    # arrange
    api_factory = ApiFactory(
        token={},
        data_access_layer=data_access_layer,
        logger=logger
    )
    admin = api_factory.create_admin_api()

    # act
    new_user_id = admin.create_user('Test User')

    # assert
    assert new_user_id == MOCK_NEW_USER_ID
