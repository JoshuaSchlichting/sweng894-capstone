from abc import ABC, abstractmethod
from typing import List


class AbstractDataAccessLayer(ABC):

    @abstractmethod
    def create_user(username: str) -> int:
        """Creates new user
        Args:
            username: name of user to create
        Return:
            id of created user
        """

    @abstractmethod 
    def cast_vote(user_id: int, election_id: int, ranked_candidate_list: List[int]) -> int:
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
    def create_candidate(username: str) -> int:
        """Creates a candidate in the system

        If a user with the same username already exists, then the existing user_id is returned.

        Return:
            id of the candidate user
        """
    
    @abstractmethod
    def create_election(election_name: str) -> int:
        """Creates a new election in the system.

        Return:
            id of the newly created election
        """
