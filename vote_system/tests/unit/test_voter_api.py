import pytest
from loguru import logger

from core.abstract_data_access_layer import AbstractDataAccessLayer
from core.api_factory import ApiFactory
from core.admin_api import AdminApi
from core.models import User
from core.models import Candidate
from core.models import Election


MOCK_USER_ID = 14234
MOCK_ELECTION_ID = 1741
MOCK_NEW_VOTE_ID = 5125


@pytest.fixture
def api(mocker):
    dal = mocker.Mock(spec=AbstractDataAccessLayer)
    dal.cast_vote.return_value = MOCK_NEW_VOTE_ID

    api_factory = ApiFactory(user_id=1, data_access_layer=dal, logger=logger)
    return api_factory.create_voter_api()


def test_cast_vote(api):
    # act
    newly_created_vote_id = api.cast_vote(
        user_id=MOCK_USER_ID,
        election_id=MOCK_ELECTION_ID,
        ranked_candidate_list=[4, 6, 3, 1, 6, 7, 8, 12, 11],
    )

    # assert
    assert newly_created_vote_id == MOCK_NEW_VOTE_ID
