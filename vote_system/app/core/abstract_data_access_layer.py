from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


class AbstractDataAccessLayer(ABC):
    @abstractmethod
    def create_user(self, username: str, password: Optional[str] = None) -> int:
        """Creates new user
        Args:
            username: name of user to create
        Return:
            id of created user
        """

    @abstractmethod
    def cast_vote(
        self, user_id: int, election_id: int, ranked_candidate_list: List[int]
    ) -> int:
        """Creates a new vote in the database

        Args:
            user_id: id of user casting vote
            election_id: id of the election vote belongs to
            ranked_candidates: and ordered list of the desired candidate ID's, with 0
                               being the highest ranked candidate.
        Return:
            id of the vote that was created
        """

    @abstractmethod
    def get_vote(self, id: int) -> dict:
        """Retrieves vote data from collection

        Args:
            id: id of vote being retrieved

        Returns:
            dict with data from collection
        """

    @abstractmethod
    def create_candidate(self, username: str) -> int:
        """Creates a candidate in the system

        If a user with the same username already exists, then the existing user_id is returned.

        Return:
            id of the candidate user
        """

    @abstractmethod
    def create_election(
        self, election_name: str, start_date: datetime, end_date: datetime
    ) -> int:
        """Creates a new election in the system.

        Args:
            election_name: self explanatory
            candidate_list: list of candidate ID's

        Return:
            id of the newly created election
        """

    @abstractmethod
    def add_candidate_to_election(self, election_id: str, candidate_id: str) -> dict:
        """Adds the candidate to the specified election"""

    @abstractmethod
    def get_election(self, id: int) -> dict:
        """Retrieves an election object

        Args:
            id: ID of the election

        Returns:
            dict of election data
        """

    @abstractmethod
    def get_all_elections(self) -> list:
        """Retrieves a list of all elections"""

    @abstractmethod
    def get_user_info_by_id(self, user_id: int) -> dict:
        """Retrieves user data from database using the user id"""

    def get_user_info_by_name(self, username: str) -> dict:
        """Retrieves user data form database using the username"""

    def get_all_candidates(self) -> list:
        """Returns a list of all candidate users"""

    def get_candidates_by_election(self, election_id: str) -> List[dict]:
        pass
