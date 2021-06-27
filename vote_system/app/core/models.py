from datetime import datetime
from dataclasses import dataclass
from typing import Set, List


@dataclass
class User:
    id: int
    name: str
    phone_number: str
    email_address: str

@dataclass
class Admin:
    pass

@dataclass
class Candidate(User):
    party: str

@dataclass
class Voter(User):
    party: str

@dataclass
class Candidate(User):
    party: str

@dataclass
class Vote:
    id: int
    cast_by: int
    ranked_candidates_list: List[int]
    timestamp_utc: datetime

@dataclass
class Election:
    id: int
    candidates: Set[int]
    votes: List[Vote]
    start_ts: datetime
    end_ts: datetime
