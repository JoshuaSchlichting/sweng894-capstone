from dataclasses import dataclass
from typing import Set

@dataclass
class Election:
    id: int
    candidates: Set[int]
