from core.abstract_api import AbstractApi


class AbstractAdminApi(AbstractApi):

    def create_user(self, username: str) -> int:
        """Create new user and return new user's ID"""
    
    def create_candidate(self, username: str) -> int:
        """Adds candidate flag to username

        If the username does not exist, a new one user will be created.

        Return:
            int representing the user id of the candidate that was created.
        """

    def create_election(self, election_name: str) -> int:
        """Creates a new election

        Return:
            id of newly created election
        """

    def declare_winner(election_id: int) -> int:
        """Prematurely ends election

        Return:
            id of candidate that has won the election.
        """
