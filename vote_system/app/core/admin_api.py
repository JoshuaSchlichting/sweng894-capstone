from datetime import datetime
from typing import Optional

from .base_api import BaseApi


class AdminApi(BaseApi):
    def create_user(
        self, username: str, user_type: str, password: Optional[str] = None
    ) -> int:
        """Create new user and return new user's ID"""
        return self._dal.create_user(
            username=username, password=password, user_type=user_type
        )

    def create_candidate(self, username: str) -> int:
        """Adds candidate flag to username

        If the username does not exist, a new one user will be created.

        Return:
            int representing the user id of the candidate that was created.
        """
        return self._dal.create_candidate(username=username)

    def create_election(
        self, election_name: str, start_date: str, end_date: str
    ) -> int:
        """Creates a new election

        Return:
            id of newly created election
        """
        return self._dal.create_election(
            election_name=election_name,
            start_date=datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(end_date, "%Y-%m-%d"),
        )

    def add_candidate_to_election(self, election_id: str, candidate_id: str) -> dict:
        """Adds candidate to an election, returning the election information"""
        return self._dal.add_candidate_to_election(
            election_id=election_id, candidate_id=candidate_id
        )

    def declare_winner(election_id: int) -> int:
        """Prematurely ends election

        Return:
            id of candidate that has won the election.
        """
        raise NotImplementedError()
