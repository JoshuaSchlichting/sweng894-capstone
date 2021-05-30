from .abstract_data_access_layer import AbstractDataAccessLayer


class ElectionFactory:

    def __init__(self, data_access_layer: AbstractDataAccessLayer, logger) -> None:
        self._dal = data_access_layer
        self._log = logger
 
    def create_election(self, election_name: str) -> int:
        return self._dal.create_election(election_name=election_name)
