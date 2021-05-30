from core.abstract_data_access_layer import AbstractDataAccessLayer


class UserFactory:

    def __init__(self, data_access_layer: AbstractDataAccessLayer, logger) -> None:
        self._dal = data_access_layer
        self._log = logger
 
    def create_new_user(self, username: id) -> int:
        return self._dal.create_user(username=username)
 