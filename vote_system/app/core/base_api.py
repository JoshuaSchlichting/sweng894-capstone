from abc import ABC

from core.abstract_data_access_layer import AbstractDataAccessLayer


class BaseApi(ABC):

    def __init__(self, token: dict, data_access_layer: AbstractDataAccessLayer, logger) -> None:
        """
        The Api's constructor should be used to determine that a user is a valid admin.

        Args:
            token: dictionary containing required credentials expected
                   for an admin user.
            data_access_layer: an implementation of AbstractDataAccessLayer
            logger: object with logging calls

        Return:
            None
        """
        self._log = logger
        self._dal = data_access_layer
        self._token = token
