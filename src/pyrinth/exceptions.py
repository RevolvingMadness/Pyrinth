"""Contains all the errors used in Pyrinth."""


class NotFoundError(Exception):

    """Used when something isn't found."""


class InvalidRequestError(Exception):

    """Used when an invalid request is sent."""

    def __init__(self, reason) -> None:
        super().__init__(f"Invalid Request. Reason: {reason}")


class NoAuthorizationError(Exception):

    """Used when a user isn't authorized."""


class InvalidParamError(Exception):

    """Used when a parameter is invalid."""
