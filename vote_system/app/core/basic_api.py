from typing import Optional

from .base_api import BaseApi


class BasicApi(BaseApi):

    def get_election(self, election_id: str) -> dict:
        return self._dal.get_election(election_id)

    def get_all_elections(self) -> list:
        return self._dal.get_all_elections()
