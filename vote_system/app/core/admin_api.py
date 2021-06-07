from .base_api import BaseApi


class AdminApi(BaseApi):
    def create_user(self, username: str) -> int:
        """Create new user and return new user's ID"""
        return self._dal.create_user(username=username)

    def create_candidate(self, username: str) -> int:
        """Adds candidate flag to username

        If the username does not exist, a new one user will be created.

        Return:
            int representing the user id of the candidate that was created.
        """
        return self._dal.create_candidate(username=username)

    def create_election(self, election_name: str) -> int:
        """Creates a new election

        Return:
            id of newly created election
        """
        return self._dal.create_election(election_name=election_name)

    def declare_winner(election_id: int) -> int:
        """Prematurely ends election

        Return:
            id of candidate that has won the election.
        """
        raise NotImplementedError()
