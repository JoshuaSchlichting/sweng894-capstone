from typing import List

import pyrankvote
from pyrankvote import Candidate, Ballot

from core.abstract_data_access_layer import AbstractDataAccessLayer


class VoteSystem:

    def __init__(self, data_access_layer: AbstractDataAccessLayer, logger) -> None:
        logger.debug("Instantiating VoteSystem")
        self._dal = data_access_layer
        self._log = logger

    def get_election_report(self, election_id: str) -> str:
        votes = self._dal.get_all_votes()
        ballots = []
        candidates = self._get_candidate_objects(election_id)
        for vote in votes:
            ranked_candidate_list = []
            for candidate_obj in vote["ranked_candidate_list"]:
                # Look, I'm not proud of this. I'm tired.    
                ranked_candidate_list.append(candidates[[str(x) for x in candidates].index(candidate_obj["id"])])
            ballots.append(Ballot(ranked_candidates=ranked_candidate_list))
        election_result = pyrankvote.instant_runoff_voting(candidates, ballots)
        self._log.debug(election_result)
        return election_result

    def _get_candidate_objects(self, election_id: str) -> List[Candidate]:
        candidates = self._dal.get_candidates_by_election(election_id)
        pyrankcandidates = []
        for candidate in candidates:
            pyrankcandidates.append(Candidate(candidate["id"]))
        return pyrankcandidates
    
