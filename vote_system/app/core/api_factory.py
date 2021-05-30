from .abstract_data_access_layer import AbstractDataAccessLayer
from .voter_api import VoterApi
from .models import UserApi
from .admin_api import AdminApi


class ApiFactory:

    def __init__(self, token: dict, data_access_layer: AbstractDataAccessLayer, logger) -> None:
        self._token = token
        self._dal = data_access_layer
        self._log = logger

    def create_voter_api(self) -> VoterApi:
        #TODO validate token for VOTERS
        return VoterApi(token=self._token, data_access_layer=self._dal, logger=self._log)
    
    def create_admin_api(self) -> AdminApi:
        #TODO validate token for ADMINS
        return AdminApi(token=self._token, data_access_layer=self._dal, logger=self._log)
    
    def create_user_api(self) -> UserApi:
        #TODO validate token for REGISTERED USERS
        return UserApi(token=self._token, data_access_layer=self._dal, logger=self._log)
