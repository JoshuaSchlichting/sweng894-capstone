from .abstract_data_access_layer import AbstractDataAccessLayer
from .voter_api import VoterApi
from .user_api import UserApi
from .admin_api import AdminApi
from .models import User


class ApiFactory:
    def __init__(
        self, user_id: int, data_access_layer: AbstractDataAccessLayer, logger
    ) -> None:
        self._user_id = user_id
        self._dal = data_access_layer
        self._log = logger

    def create_voter_api(self) -> VoterApi:
        # TODO validate token for VOTERS
        return VoterApi(
            user_id=self._user_id, data_access_layer=self._dal, logger=self._log
        )

    def create_admin_api(self) -> AdminApi:
        # TODO validate token for ADMINS
        return AdminApi(
            user_id=self._user_id, data_access_layer=self._dal, logger=self._log
        )

    def create_user_api(self) -> UserApi:
        # TODO validate token for REGISTERED USERS
        return UserApi(user_id=self._user_id, data_access_layer=self._dal, logger=self._log)
