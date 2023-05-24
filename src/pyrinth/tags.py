import requests as _requests
import pyrinth.exceptions as _exceptions


class Tag:
    @classmethod  # type: ignore
    @property
    def categories(self) -> list["Tag._Category"]:
        """
        Gets a list of tag categories

        Returns:
            (list[Tag.Category]): A list of tag categories

        Raises:
            exceptions.InvalidRequestError: If the request to the API fails
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/category", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return [
            Tag._Category(
                json.get("icon"),
                json.get("name"),
                json.get("project_type"),
                json.get("header"),
            )
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def loaders(self) -> list["Tag._Loaders"]:
        """
        Gets a list of tag loaders

        Returns:
            (list[Tag.Loader]): A list of tag loaders

        Raises:
            exceptions.InvalidRequestError: If the request to the API fails
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/loader", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return [
            Tag._Loaders(
                json.get("icon"), json.get("name"), json.get("supported_project_types")
            )
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def game_versions(self) -> list["Tag._GameVersion"]:
        """
        Gets a list of tag game versions

        Returns:
            (list[Tag.GameVersion]): A list of tag game versions

        Raises:
            (InvalidRequestError): If the request to the API fails
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/game_version", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return [
            Tag._GameVersion(
                json.get("version"),
                json.get("version_type"),
                json.get("date"),
                json.get("major"),
            )
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def licenses(self) -> list["Tag._License"]:
        """
        Gets a list of tag licenses

        Returns:
            (list[Tag.License]): A list of tag licenses

        Raises:
            exceptions.InvalidRequestError: If the request to the API fails
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/license", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return [Tag._License(json.get("short"), json.get("name")) for json in response]

    @classmethod  # type: ignore
    @property
    def donation_platforms(self) -> list["Tag._DonationPlatform"]:
        """
        Gets a list of tag donation platforms

        Returns:
            (list[Tag.DonationPlatform]): A list of tag donation platforms

        Raises:
            exceptions.InvalidRequestError: If the request to the API fails
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/donation_platform", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return [
            Tag._DonationPlatform(json.get("short"), json.get("name"))
            for json in response
        ]

    @classmethod  # type: ignore
    @property
    def report_types(self) -> list[str]:
        """
        Gets a list of tag report types

        Returns:
            (list[str]): A list of tag report types

        Raises:
            exceptions.InvalidRequestError: If the request to the API fails
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/tag/report_type", timeout=60
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return response

    class _Category:
        """
        Represents a tag category

        Attributes:
            icon (str): The icon for the category
            name (str): The name of the category
            project_type (str): The project type for the category
            header (str): The header for the category

        """

        def __init__(
            self, icon: str, name: str, project_type: str, header: str
        ) -> None:
            """
            Initializes a Category object

            Args:
                icon (str): The icon for the category
                name (str): The name of the category
                project_type (str): The project type for the category
                header (str): The header for the category
            """
            self.icon = icon
            self.name = name
            self.project_type = project_type
            self.header = header

        def __repr__(self) -> str:
            return f"Category: {self.name}"

    class _Loaders:
        """
        Represents a tag loader

        Attributes:
            icon (str): The icon for the loader
            name (str): The name of the loader
            supported_project_types (list[str]): A list of supported project types for the loader

        """

        def __init__(
            self, icon: str, name: str, supported_project_types: list[str]
        ) -> None:
            """
            Initializes a Loader object

            Args:
                icon (str): The icon for the loader
                name (str): The name of the loader
                supported_project_types (list[str]): A list of supported project types for the loader
            """
            self.icon = icon
            self.name = name
            self.supported_project_types = supported_project_types

        def __repr__(self) -> str:
            return f"Loader: {self.name}"

    class _GameVersion:
        """
        Represents a tag game version

        Attributes:
            version (str): The version of the game
            version_type (str): The type of the version
            date (str): The date of the version
            major (bool): Whether the version is a major version or not

        """

        def __init__(
            self, version: str, version_type: str, date: str, major: bool
        ) -> None:
            """
            Initializes a GameVersion object

            Args:
                version (str): The version of the game
                version_type (str): The type of the version
                date (str): The date of the version
                major (bool): Whether the version is a major version or not
            """
            self.version = version
            self.version_type = version_type
            self.date = date
            self.major = major

        def __repr__(self) -> str:
            return f"Game Version: {self.version}"

    class _License:
        """
        Represents a tag license

        Attributes:
            short (str): The short name of the license
            name (str): The name of the license

        """

        def __init__(self, short: str, name: str) -> None:
            """
            Initializes a License object

            Args:
                short (str): The short name of the license
                name (str): The name of the license
            """
            self.short = short
            self.name = name

        def __repr__(self) -> str:
            return f"License: {self.name}"

    class _DonationPlatform:
        """
        Represents a tag donation platform

        Attributes:
            short (str): The short name of the donation platform
            name (str): The name of the donation platform

        """

        def __init__(self, short: str, name: str) -> None:
            """
            Initializes a DonationPlatform object

            Args:
                short (str): The short name of the donation platform
                name (str): The name of the donation platform
            """
            self.short = short
            self.name = name

        def __repr__(self) -> str:
            return f"Donation Platform: {self.name}"
