from typing import Optional

from .base_api import BaseApi


class BasicApi(BaseApi):

    def get_election(self, election_id: str) -> dict:
        return self._dal.get_election(election_id)
