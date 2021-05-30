from dataclasses import dataclass

from core.user import User


class Candidate(User):
    party: str
