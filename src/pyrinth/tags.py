import dataclasses

import requests as _requests

import pyrinth.exceptions as _exceptions


class Tag:
    @classmethod  # type: ignore
    @property
    def categories(cls) -> list["Tag._Category"]:
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/category", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: list[dict] = raw_response.json()
        return [
            Tag._Category(
                json.get("icon", ...),
                json.get("name", ...),
                json.get("project_type", ...),
                json.get("header", ...),
            )
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def loaders(cls) -> list["Tag._Loaders"]:
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/loader", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: list[dict] = raw_response.json()
        return [
            Tag._Loaders(
                json.get("icon", ...),
                json.get("name", ...),
                json.get("supported_project_types", ...),
            )
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def game_versions(cls) -> list["Tag._GameVersion"]:
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/game_version", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: list[dict] = raw_response.json()
        return [
            Tag._GameVersion(
                json.get("version", ...),
                json.get("version_type", ...),
                json.get("date", ...),
                json.get("major", ...),
            )
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def licenses(cls) -> list["Tag._License"]:
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/license", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: list[dict] = raw_response.json()
        return [
            Tag._License(json.get("short", ...), json.get("name", ...))
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def donation_platforms(cls) -> list["Tag._DonationPlatform"]:
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/donation_platform", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: list[dict] = raw_response.json()
        return [
            Tag._DonationPlatform(json.get("short", ...), json.get("name", ...))
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def report_types(cls) -> list[str]:
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/report_type", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: list = raw_response.json()
        return response

    @dataclasses.dataclass
    class _Category:
        """
        Represents a tag category.

        Attributes:
            icon (str): The icon for the category
            name (str): The name of the category
            project_type (str): The project type for the category
            header (str): The header for the category

        """

        icon: str
        name: str
        project_type: str
        header: str

        def __repr__(self) -> str:
            return f"Category: {self.name}"

    @dataclasses.dataclass
    class _Loaders:
        """
        Represents a tag loader.

        Attributes:
            icon (str): The icon for the loader
            name (str): The name of the loader
            supported_project_types (list[str]): A list of supported project types for the loader

        """

        icon: str
        name: str
        supported_project_types: list

        def __repr__(self) -> str:
            return f"Loader: {self.name}"

    @dataclasses.dataclass
    class _GameVersion:
        """
        Represents a tag game version.

        Attributes:
            version (str): The version of the game
            version_type (str): The type of the version
            date (str): The date of the version
            major (bool): Whether the version is a major version or not

        """

        version: str
        version_type: str
        data: str
        major: bool

        def __repr__(self) -> str:
            return f"Game Version: {self.version}"

    @dataclasses.dataclass
    class _License:
        """
        Represents a tag license.

        Attributes:
            short (str): The short name of the license
            name (str): The name of the license

        """

        short: str
        name: str

        def __repr__(self) -> str:
            return f"License: {self.name}"

    @dataclasses.dataclass
    class _DonationPlatform:
        """
        Represents a tag donation platform.

        Attributes:
            short (str): The short name of the donation platform
            name (str): The name of the donation platform

        """

        short: str
        name: str

        def __repr__(self) -> str:
            return f"Donation Platform: {self.name}"
