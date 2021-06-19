from datetime import datetime
from dataclasses import dataclass
from typing import Set, List


@dataclass
class User:
    id: int
    name: str
    phone_number: str
    email_address: str
    user_type: str


@dataclass
class Candidate(User):
    party: str


@dataclass
class Voter(User):
    pass


@dataclass
class Candidate(User):
    party: str


@dataclass
class Election:
    id: int
    candidates: Set[int]
    start_ts: datetime
    end_ts: datetime


@dataclass
class Vote:
    id: int
    cast_by: int
    ranked_candidates_list: List[int]
    timestamp_utc: datetime
