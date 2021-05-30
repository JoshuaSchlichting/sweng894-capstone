from typing import List

from .base_api import BaseApi


class VoterApi(BaseApi):

    def cast_vote(self, user_id: int, election_id: int, ranked_candidate_list: List[int]) -> int:
        """Casts a users vote

        Return:
            ID of the vote generated
        """
        return self._dal.cast_vote(
            user_id=user_id,
            election_id=election_id,
            ranked_candidate_list=ranked_candidate_list
        )
