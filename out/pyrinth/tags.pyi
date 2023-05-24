from _typeshed import Incomplete

class Tag:
    @classmethod
    @property
    def categories(self) -> list['Tag._Category']: ...
    @classmethod
    @property
    def loaders(self) -> list['Tag._Loaders']: ...
    @classmethod
    @property
    def game_versions(self) -> list['Tag._GameVersion']: ...
    @classmethod
    @property
    def licenses(self) -> list['Tag._License']: ...
    @classmethod
    @property
    def donation_platforms(self) -> list['Tag._DonationPlatform']: ...
    @classmethod
    @property
    def report_types(self) -> list[str]: ...
    class _Category:
        icon: Incomplete
        name: Incomplete
        project_type: Incomplete
        header: Incomplete
        def __init__(self, icon: str, name: str, project_type: str, header: str) -> None: ...
    class _Loaders:
        icon: Incomplete
        name: Incomplete
        supported_project_types: Incomplete
        def __init__(self, icon: str, name: str, supported_project_types: list[str]) -> None: ...
    class _GameVersion:
        version: Incomplete
        version_type: Incomplete
        date: Incomplete
        major: Incomplete
        def __init__(self, version: str, version_type: str, date: str, major: bool) -> None: ...
    class _License:
        short: Incomplete
        name: Incomplete
        def __init__(self, short: str, name: str) -> None: ...
    class _DonationPlatform:
        short: Incomplete
        name: Incomplete
        def __init__(self, short: str, name: str) -> None: ...
