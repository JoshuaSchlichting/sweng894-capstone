from dataclasses import dataclass

from .models import User


class Candidate(User):
    party: str
