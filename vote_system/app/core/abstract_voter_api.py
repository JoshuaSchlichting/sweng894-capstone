from typing import List

from core.abstract_api import AbstractApi


class AbstractVoterApi(AbstractApi):

    def cast_vote(user_id: int, election_id: int, ranked_candidate_list: List[int]) -> int:
        """Casts a users vote

        Return:
            ID of the vote generated
        """
