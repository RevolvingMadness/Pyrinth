"""Contains all models used in Pyrinth."""

import json

import pyrinth.literals as literals
import pyrinth.projects as projects
import pyrinth.util as util


class ProjectModel:
    """The model used for the Project class.

    Attributes:
        slug (str): The slug of the project.
        title (str): The title of the project.
        description (str): The description of the project.
        categories (list[str]): The categories of the project.
        client_side (str): The client side of the project.
        server_side (str): The server side of the project.
        body (str): The body of the project.
        license (Project.License): The license of the project.
        project_type (str): The type of the project.
        additional_categories (list[str]): Additional categories for the project.
        issues_url (str): URL for issues related to the project.
        source_url (str): URL for the source code of the project.
        wiki_url (str): URL for the wiki page of the project.
        discord_url (str): URL for the Discord server of the project.
        auth (str): Authentication token for the project.
    """

    def __init__(
        self,
        slug: str,
        title: str,
        description: str,
        categories: list[str],
        client_side: str,
        server_side: str,
        body: str,
        license_: "projects.Project.License",
        project_type: str,
        additional_categories: list[str] | None = None,
        issues_url: str | None = None,
        source_url: str | None = None,
        wiki_url: str | None = None,
        discord_url: str | None = None,
        auth: str | None = None,
    ) -> None:
        """Initializes a new instance of ProjectModel.

        Args:
            slug (str): The slug of the project.
            title (str): The title of the project.
            description (str): The description of the project.
            categories (list[str]): The categories of the project.
            client_side (str): The client side of the project.
            server_side (str): The server side of the project.
            body (str): The body of the project.
            license_ (Project.License): The license of the project.
            project_type (str): The type of the project.
            additional_categories (list[str], optional): Additional categories for the project. Defaults to None.
            issues_url (str, optional): URL for issues related to the project. Defaults to None.
            source_url (str, optional): URL for the source code of the project. Defaults to None.
            wiki_url (str, optional): URL for the wiki page of the project. Defaults to None.
            discord_url (str, optional): URL for Discord server related to this project. Defaults to None.
            auth (str, optional): Authentication token for this instance. Defaults to None.
        """
        self.slug = slug
        self.title = title
        self.description = description
        self.categories = categories
        self.client_side = client_side
        self.server_side = server_side
        self.body = body
        self.license = license_._to_json()
        self.project_type = project_type
        self.additional_categories = additional_categories
        self.issues_url = issues_url
        self.source_url = source_url
        self.wiki_url = wiki_url
        self.discord_url = discord_url
        self.donation_urls = None
        self.auth = auth
        self.id = None
        self.downloads = None
        self.icon_url = None
        self.color = None
        self.team = None
        self.moderator_message = None
        self.published = None
        self.updated = None
        self.approved = None
        self.followers = None
        self.status = None
        self.version_ids = None
        self.game_versions = None
        self.loaders = None
        self.gallery = None

    @staticmethod
    def _from_json(json_: dict) -> "ProjectModel":
        license_ = projects.Project.License._from_json(json_.get("license"))  # type: ignore

        result = ProjectModel(
            json_.get("slug"),  # type: ignore
            json_.get("title"),  # type: ignore
            json_.get("description"),  # type: ignore
            json_.get("categories"),  # type: ignore
            json_.get("client_side"),  # type: ignore
            json_.get("server_side"),  # type: ignore
            json_.get("body"),  # type: ignore
            license_,
            json_.get("project_type"),  # type: ignore
            json_.get("additional_categories"),  # type: ignore
            json_.get("issues_url"),  # type: ignore
            json_.get("source_url"),  # type: ignore
            json_.get("wiki_url"),  # type: ignore
            json_.get("discord_url"),  # type: ignore
            json_.get("authorization"),
        )
        result.id = json_.get("id")
        result.downloads = json_.get("downloads")
        result.donation_urls = json_.get("donation_urls")
        result.icon_url = json_.get("icon_url")
        result.color = json_.get("color")
        result.team = json_.get("team")
        result.moderator_message = json_.get("moderator_message")
        result.published = json_.get("published")
        result.updated = json_.get("updated")
        result.approved = json_.get("approved")
        result.followers = json_.get("followers")
        result.status = json_.get("status")
        result.version_ids = json_.get("versions")
        result.game_versions = json_.get("game_versions")
        result.loaders = json_.get("loaders")
        result.gallery = json_.get("gallery")
        return result

    def _to_json(self) -> dict:
        return util.remove_null_values(self.__dict__)

    def _to_bytes(self) -> bytes:
        return json.dumps(self._to_json()).encode()


class SearchResultModel:
    """The model used for the SearchResult class.

    Attributes:
        slug (str): The slug of the search result.
        title (str): The title of the search result.
        description (str): The description of the search result.
        client_side (str): The client side of the search result.
        server_side (str): The server side of the search result.
        project_type (str): The type of the search result.
        downloads (int): The number of downloads for the search result.
        project_id (str): The ID of the project associated with the search result.
        author (str): The author of the search result.
        versions (list[str]): The versions associated with the search result.
        follows (int): The number of follows for the search result.
        date_created (str): The date when the search result was created.
        date_modified (str): The date when the search result was last modified.
        license (str): The license associated with the search result.
        categories (list[str]): The categories associated with the search result.
        icon_url (str): The URL for the icon associated with the search result.
        color (str): The color associated with the search result.
        display_categories (list[str]): The categories to display for the search result.
        latest_version (str): The latest version associated with the search result.
        gallery (list[str]): The gallery associated with the search result.
        featured_gallery (list[str]): The featured gallery associated with the search result.

    """

    def __init__(self) -> None:
        self.slug: str | None = None
        self.title: str | None = None
        self.description: str | None = None
        self.client_side: str | None = None
        self.server_side: str | None = None
        self.project_type: str | None = None
        self.downloads: int | None = None
        self.project_id: str | None = None
        self.author: str | None = None
        self.versions: list[str] | None = None
        self.follows: int | None = None
        self.date_created = None
        self.date_modified = None
        self.license: str | None = None
        self.categories: list[str] | None = None
        self.icon_url: str | None = None
        self.color: str | None = None
        self.display_categories: list[str] | None = None
        self.latest_version: list[str] | None = None
        self.gallery: list[str] | None = None
        self.featured_gallery: list[str] | None = None

    @staticmethod
    def _from_json(json_: dict) -> "SearchResultModel":
        result = SearchResultModel()
        result.slug = json_.get("slug")
        result.title = json_.get("title")
        result.description = json_.get("description")
        result.client_side = json_.get("client_side")
        result.server_side = json_.get("server_side")
        result.project_type = json_.get("project_type")
        result.downloads = json_.get("downloads")
        result.project_id = json_.get("project_id")
        result.author = json_.get("author")
        result.versions = json_.get("versions")
        result.follows = json_.get("follows")
        result.date_created = json_.get("date_created")
        result.date_modified = json_.get("date_modified")
        result.license = json_.get("license")
        result.categories = json_.get("categories")
        result.icon_url = json_.get("icon_url")
        result.color = json_.get("color")
        result.display_categories = json_.get("display_categories")
        result.latest_version = json_.get("latest_version")
        result.gallery = json_.get("gallery")
        result.featured_gallery = json_.get("featured_gallery")

        return result

    def _to_json(self) -> dict:
        return util.remove_null_values(self.__dict__)

    def _to_bytes(self) -> bytes:
        return json.dumps(self._to_json()).encode()


class VersionModel:
    """The model used for the Version class.

    Attributes:
        name (str): The name of the version.
        version_number (str): The version number of the version.
        dependencies (list[Project.Dependency]): The dependencies of the version.
        game_versions (list[str]): The game versions associated with the version.
        version_type (version_type_literal): The type of the version.
        loaders (list[str]): The loaders associated with the version.
        featured (bool): Whether the version is featured.
        files (list[str]): The file parts associated with the version.
        changelog (str, optional): The changelog for the version. Defaults to None.
        status (version_status_literal, optional): The status of the version. Defaults to None.
        requested_status (requested_version_status_literal, optional): The requested status of the version. Defaults to None.

    """

    def __init__(
        self,
        name: str,
        version_number: str,
        dependencies: list["projects.Project.Dependency"],
        game_versions: list[str],
        version_type: literals.version_type_literal,
        loaders: list[str],
        featured: bool,
        file_parts: list[str],
        changelog: str | None = None,
        status: literals.version_status_literal | None = None,
        requested_status: literals.requested_version_status_literal | None = None,
    ) -> None:
        """
        Initializes a new instance of VersionModel.

        Args:
            name (str): The name of the version.
            version_number (str): The version number of the version.
            dependencies (list[projects.Project.Dependency]): The dependencies of the version.
            game_versions (list[str]): The game versions associated with the version.
            version_type (version_type_literal): The type of the version.
            loaders (list[str]): The loaders associated with the version.
            featured (bool): Whether the version is featured.
            file_parts (list[str]): The file parts associated with the version.
            changelog (str, optional): The changelog for the version. Defaults to None.
            status (version_status_literal, optional): The status of the version. Defaults to None.
            requested_status (requested_version_status_literal, optional): The requested status of the version. Defaults to None.
        """
        self.name = name
        self.version_number = version_number
        self.changelog = changelog
        self.dependencies = util.list_to_json(dependencies)
        self.game_versions = game_versions
        self.version_type = version_type
        self.loaders = loaders
        self.featured = featured
        self.status = status
        self.requested_status = requested_status
        self.files = file_parts
        self.project_id = None
        self.id = None
        self.author_id = None
        self.date_published = None
        self.downloads = None

    @staticmethod
    def _from_json(json_: dict) -> "VersionModel":
        result = VersionModel(
            json_.get("name"),  # type: ignore
            json_.get("version_number"),  # type: ignore
            json_.get("dependencies"),  # type: ignore
            json_.get("game_versions"),  # type: ignore
            json_.get("version_type"),  # type: ignore
            json_.get("loaders"),  # type: ignore
            json_.get("featured"),  # type: ignore
            json_.get("files"),  # type: ignore
            json_.get("changelog"),  # type: ignore
            json_.get("status"),  # type: ignore
            json_.get("requested_status"),  # type: ignore
        )
        result.project_id = json_.get("project_id")
        result.id = json_.get("id")
        result.author_id = json_.get("author_id")
        result.date_published = json_.get("date_published")
        result.downloads = json_.get("downloads")
        return result

    def _to_json(self) -> dict:
        return util.remove_null_values(self.__dict__)

    def _to_bytes(self) -> bytes:
        return json.dumps(self._to_json()).encode()


class UserModel:
    """The model used for the User class.

    Attributes:
        username (str, optional): The username of the user.
        id (str, optional): The ID of the user.
        avatar_url (str, optional): The URL for the avatar of the user.
        created (str, optional): The date when the user was created.
        role (str, optional): The role of the user.
        name (str, optional): The name of the user.
        email (str, optional): The email address of the user.
        bio (str, optional): The bio of the user.
        payout_data (UNKNOWN, optional): The payout data for the user.
        github_id (int, optional): The GitHub ID of the user.
        badges (list[str], optional): The badges associated with the user.
        auth (str, optional): Authentication information for the user.

    """

    def __init__(self) -> None:
        self.username: str | None = None
        self.id: str | None = None
        self.avatar_url: str | None = None
        self.created: str | None = None
        self.role: str | None = None
        self.name: str | None = None
        self.email: str | None = None
        self.bio: str | None = None
        self.payout_data = None
        self.github_id: int | None = None
        self.badges: list[str] | None = None
        self.auth: str | None = None

    @staticmethod
    def _from_json(json_: dict) -> "UserModel":
        result = UserModel()
        result.username = json_.get("username")
        result.id = json_.get("id")
        result.avatar_url = json_.get("avatar_url")
        result.created = json_.get("created")
        result.role = json_.get("role")
        result.name = json_.get("name")
        result.email = json_.get("email")
        result.bio = json_.get("bio")
        result.payout_data = json_.get("payout_data")
        result.github_id = json_.get("github_id")
        result.badges = json_.get("badges")
        result.auth = json_.get("authorization", "")

        return result

    def _to_json(self) -> dict:
        return util.remove_null_values(self.__dict__)

    def _to_bytes(self) -> bytes:
        return json.dumps(self._to_json()).encode()
