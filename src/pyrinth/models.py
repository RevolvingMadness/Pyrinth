"""Contains all models used in Pyrinth."""

import json

import pyrinth.literals as literals
import pyrinth.projects as projects
import pyrinth.util as util


class ProjectModel:
    """The model used for the Project class

    Attributes:
        slug (str): The slug of the project, used for vanity URLs. Regex: ^[\\w!@$()`.+,"\\-']{3,64}$
        title (str): The title or name of the project
        description (str): A short description of the project
        categories (list[str]): A list of categories that the project has
        client_side (str): The client side support of the project
        server_side (str): The server side support of the project
        body (str): A long form description of the project
        additional_categories (list[str]): A list of categories which are searchable but non-primary
        issues_url (str): An optional link to where to submit bugs or issues with the project
        source_url (str): An optional link to the source code of the project
        wiki_url (str): An optional link to the project's wiki page or other relevant information
        discord_url (str): An optional invite link to the project's discord
        donation_urls (list[dict]): A list of donations for the project
        project_type (str): The project type
        downloads (int): The total number of downloads of the project
        icon_url (str): The URL of the project's icon
        color (str): The RGB color of the project, automatically generated from the project icon
        id (str): The ID of the project, encoded as a base62 string
        team (str): The ID of the team that has ownership of this project
        moderator_message: A message that a moderator sent regarding the project
        published (str): The date the project was published
        updated (str): The date the project was last updated
        approved (str): The date of the project's status was set to approved or unlisted
        followers (int): The total number of users following the project
        status (str): The status of the project
        license (dict): The license of the project
        version_ids (list[str]): A list of version IDs of the project (will never be empty unless draft status)
        game_versions (list[str]): A list of all the game versions supported by the project
        loaders (list[str]): A list of all the loaders supported by the project
        gallery (list[dict]): A list of images that have been uploaded to the project's gallery
        auth (str): The project's authorization token
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
        """Initializes a new instance of ProjectModel

        Args:
            slug (str): The slug of the project, used for vanity URLs. Regex: ^[\\w!@$()`.+,"\\-']{3,64}$
            title (str): The title or name of the project
            description (str): A short description of the project
            categories (list[str]): A list of categories that the project has
            client_side (str): The client side support of the project
            server_side (str): The server side support of the project
            body (str): A long form description of the project
            license_ (Project.License): The license of the project
            project_type (str): The project type
            additional_categories (list[str], optional): A list of categories which are searchable but non-primary
            issues_url (str, optional): An optional link to where to submit bugs or issues with the project
            source_url (str, optional): An optional link to the source code of the project
            wiki_url (str, optional): An optional link to the project's wiki page or other relevant information
            discord_url (str, optional): An optional invite link to the project's discord
            auth (str, optional): Authentication token for the project
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
        self.donation_urls: list[dict] | None = None
        self.auth = auth
        self.id: str | None = None
        self.downloads: int | None = None
        self.icon_url: str | None = None
        self.color: str | None = None
        self.team: str | None = None
        self.moderator_message = None
        self.published: str | None = None
        self.updated: str | None = None
        self.approved: str | None = None
        self.followers: int | None = None
        self.status: str | None = None
        self.version_ids: list[str] | None = None
        self.game_versions: list[str] | None = None
        self.loaders: list[str] | None = None
        self.gallery: list[dict] | None = None

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
    """The model used for the SearchResult class

    Attributes:
        slug (str): The slug of a project, used for vanity URLs. Regex: ^[\\w!@$()`.+,"\\-']{3,64}$
        title (str): The title or name of the project
        description (str): A short description of the project
        client_side (str): The client side support of the project
        server_side (str): The server side support of the project
        project_type (str): The project type
        downloads (int): The total number of downloads of the project
        project_id (str): The ID of the project
        author (str): The username of the project's author
        versions (list[str]): A list of the minecraft versions supported by the project
        follows (int): The total number of users following the project
        date_created (str): The date the project was added to search
        date_modified (str): The date the project was last modified
        license (str): The SPDX license ID of the project
        categories (list[str]): A list of categories that the project has
        icon_url (str): The URL of the project's icon
        color (str): The RGB color of the project, automatically generated from the project icon
        display_categories (list[str]): A list of categories that the project has which are not secondary
        latest_version (str): The latest version of minecraft that this project supports
        gallery (list[str]): All gallery images attached to the project
        featured_gallery (list[str]): The featured gallery image of the project

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
    """The model used for the Version class

    Attributes:
        name (str): The name of this version
        version_number (str): The version number. Ideally will follow semantic versioning
        changelog (str): The changelog for this version
        dependencies (list[dict]): A list of specific versions of projects that this version depends on
        game_versions (list[str]): A list of versions of Minecraft that this version supports
        version_type (str): The release channel for this version
        loaders (list[str]): The mod loaders that this version supports
        featured (bool): Whether the version is featured or not
        status (str): The version's status
        requested_status (str): The version's requested status
        files (list[dict]): A list of files avaliable for download for this version
        project_id (str): The ID of the project this version is for
        id (str): The ID of the version, encoded as base62 string
        author_id (str): The ID of the author who published this version
        date_published (str): When the version was published
        downloads (int): The number of times this version has been downloaded

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
        Initializes a new instance of VersionModel

        Args:
            name (str): The name of this version
            version_number (str): The version number. Ideally will follow semantic versioning
            dependencies (list[Project.Dependency]): A list of specific versions of projects that this version depends on
            game_versions (list[str]): A list of versions of Minecraft that this version supports
            version_type (Literal["release", "beta", "alpha"]): The release channel for this version
            loaders (list[str]): The mod loaders that this version supports
            featured (bool): Whether the version is featured or not
            file_parts (list[str]): A list of files avaliable for download for this version
            changelog (str, optional): The changelog for this version
            status (Literal["listed", "archived", "draft", "unlisted", "scheduled", "unknown"], optional): The version's status
            requested_status (Literal["listed", "archived", "draft", "unlisted"], optional): The version's requested status
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
    """The model used for the User class

    Attributes:
        username (str): The user's username
        id (str): The user's ID
        avatar_url (str): The user's avatar URL
        created (str): The time at which the user was created
        role (str): The user's role
        name (str): The user's display name
        email (str): The user's email (only when your own is ever displayed)
        bio (str): A description of the user
        payout_data (): Various data relating to the user's payouts status (you can only see your own)
        github_id (int): The user's GitHub ID
        badges (list[str]): Any badges applicable to this user. These are currently unused and undisplayed, and as such are subject to change
        auth (str): Authentication token for the user
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
