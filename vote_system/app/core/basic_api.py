from typing import List

from .base_api import BaseApi


class BasicApi(BaseApi):
    def get_election(self, election_id: str) -> dict:
        return self._dal.get_election(election_id)

    def get_all_elections(self) -> list:
        return self._dal.get_all_elections()

    def get_all_candidates(self) -> list:
        return self._dal.get_all_candidates()

    def get_candidates_by_election(self, election_id: str) -> List[dict]:
        return self._dal.get_candidates_by_election(election_id=election_id)
