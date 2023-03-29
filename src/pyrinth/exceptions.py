"""Contains all of the errors used in Pyrinth"""


class NotFoundError(Exception):
    """Used when a 404 occurs"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidRequestError(Exception):
    """Used when a 400 occurs"""

    def __init__(self) -> None:
        super().__init__("Invalid Request")


class NoAuthorization(Exception):
    """Used when a 401 occurs"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidParamError(Exception):
    """Used when a 400 occurs"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
