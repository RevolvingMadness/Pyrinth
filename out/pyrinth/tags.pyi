from _typeshed import Incomplete

class Tag:
    @staticmethod
    def get_categories() -> list['Tag.Category']: ...
    @staticmethod
    def get_loaders() -> list['Tag.Loader']: ...
    @staticmethod
    def get_game_versions() -> list['Tag.GameVersion']: ...
    @staticmethod
    def get_licenses() -> list['Tag.License']: ...
    @staticmethod
    def get_donation_platforms() -> list['Tag.DonationPlatform']: ...
    @staticmethod
    def get_report_types() -> list[str]: ...
    class Category:
        icon: Incomplete
        name: Incomplete
        project_type: Incomplete
        header: Incomplete
        def __init__(self, icon: str, name: str, project_type: str, header: str) -> None: ...
    class Loader:
        icon: Incomplete
        name: Incomplete
        supported_project_types: Incomplete
        def __init__(self, icon: str, name: str, supported_project_types: list[str]) -> None: ...
    class GameVersion:
        version: Incomplete
        version_type: Incomplete
        date: Incomplete
        major: Incomplete
        def __init__(self, version: str, version_type: str, date: str, major: bool) -> None: ...
    class License:
        short: Incomplete
        name: Incomplete
        def __init__(self, short: str, name: str) -> None: ...
    class DonationPlatform:
        short: Incomplete
        name: Incomplete
        def __init__(self, short: str, name: str) -> None: ...
