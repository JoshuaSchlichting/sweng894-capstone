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
class Election:
    id: int
    candidates: Set[int]


@dataclass
class Vote:
    id: int
    cast_by: int
    ranked_candidates_list: List[int]
    timestamp_utc: datetime
