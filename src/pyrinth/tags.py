import requests as r
from pyrinth.exceptions import *


class Tag:
    """Used for getting Modrinth tags."""

    @staticmethod
    def get_categories() -> list['Tag.Category']:
        """Get a list of categories."""
        raw_response = r.get(
            'https://api.modrinth.com/v2/tag/category',
            timeout=60
        )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = raw_response.json()
        return [Tag.Category(json["icon"], json["name"], json["project_type"], json["header"]) for json in response]

    @staticmethod
    def get_loaders() -> list['Tag.Loader']:
        """Get a list of loaders."""
        raw_response = r.get(
            'https://api.modrinth.com/v2/tag/loader',
            timeout=60
        )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = raw_response.json()
        return [Tag.Loader(json["icon"], json["name"], json["supported_project_types"]) for json in response]

    @staticmethod
    def get_game_versions() -> list['Tag.GameVersion']:
        """Get a list of game versions."""
        raw_response = r.get(
            'https://api.modrinth.com/v2/tag/game_version',
            timeout=60
        )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = raw_response.json()
        return [Tag.GameVersion(json["version"], json["version_type"], json["date"], json["major"]) for json in response]

    @staticmethod
    def get_licenses() -> list['Tag.License']:
        """Get a list of licenses."""
        raw_response = r.get(
            'https://api.modrinth.com/v2/tag/license',
            timeout=60
        )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = raw_response.json()
        return [Tag.License(json["short"], json["name"]) for json in response]

    @staticmethod
    def get_donation_platforms() -> list['Tag.DonationPlatform']:
        """Get a list of donation platforms."""
        raw_response = r.get(
            'https://api.modrinth.com/v2/tag/donation_platform',
            timeout=60
        )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = raw_response.json()
        return [Tag.DonationPlatform(json["short"], json["name"]) for json in response]

    @staticmethod
    def get_report_types() -> list[str]:
        """Get a list of report types."""
        raw_response = r.get(
            'https://api.modrinth.com/v2/tag/report_type',
            timeout=60
        )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = raw_response.json()
        return response

    class Category:
        """Category tag."""

        def __init__(self, icon, name, project_type, header) -> None:
            self.icon = icon
            self.name = name
            self.project_type = project_type
            self.header = header

    class Loader:
        """Loader tag."""

        def __init__(self, icon, name, supported_project_types) -> None:
            self.icon = icon
            self.name = name
            self.supported_project_types = supported_project_types

    class GameVersion:
        """Game version tag."""

        def __init__(self, version, version_type, date, major) -> None:
            self.version = version
            self.version_type = version_type
            self.date = date
            self.major = major

    class License:
        """License tag."""

        def __init__(self, short, name) -> None:
            self.short = short
            self.name = name

    class DonationPlatform:
        """Donation platform tag."""

        def __init__(self, short, name) -> None:
            self.short = short
            self.name = name