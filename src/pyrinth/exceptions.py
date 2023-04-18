"""Contains all the errors used in Pyrinth."""


class NotFoundError(Exception):
    """Used when a 404 occurs."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidRequestError(Exception):
    """Used when a 400 occurs."""

    def __init__(self, reason) -> None:
        super().__init__(f"Invalid Request. Reason: {reason}")


class NoAuthorizationError(Exception):
    """Used when a 401 occurs."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidParamError(Exception):
    """Used when a 400 occurs."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
