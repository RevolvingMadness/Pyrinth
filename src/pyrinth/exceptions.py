class NotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidRequest(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid Request")


class NoAuthorization(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidInput(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidParam(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
