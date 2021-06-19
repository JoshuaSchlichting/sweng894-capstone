from .abstract_data_access_layer import AbstractDataAccessLayer
from .models import User, Candidate, Voter


class UserFactory:
    def __init__(self, data_access_layer: AbstractDataAccessLayer, logger) -> None:
        self._dal = data_access_layer
        self._log = logger

    def get_user(self, user_id: int) -> User:
        user_info = self._dal.get_user_info(id=user_id)
        return self._create_user(
            user_id=user_info["id"],
            username=user_info["username"],
            phone_number=user_info["phone_number"],
            email_address=user_info["email_address"]
        )

    def _create_user(self, user_id: int, username: str, user_type: str, phone_number: str, email: str) -> User:
        if user_type == 'user':
            return User(id=user_id, name=username, phone_number=phone_number, email_address=email)
