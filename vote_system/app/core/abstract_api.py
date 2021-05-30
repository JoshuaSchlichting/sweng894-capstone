from abc import ABC


class AbstractApi(ABC):

    def __init__(self, token: dict) -> None:
        """
        The Api's constructor should be used to determine that a user is a valid admin.

        Args:
            token: dictionary containing required credentials expected
                   for an admin user.

        Return:
            None
        """
