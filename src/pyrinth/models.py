"""Contains all models used in Pyrinth."""
from __future__ import annotations

import json as _json

import pyrinth.literals as _literals
import pyrinth.projects as _projects
import pyrinth.util as _util


class _Model:
    def _to_json(self) -> dict:
        return _util.remove_null_values(self.__dict__)

    def _to_bytes(self) -> bytes:
        return _json.dumps(self._to_json()).encode()


class ProjectModel(_Model):
    r"""The model used for the Project class.

    Attributes:
        slug (str): The slug of the project, used for vanity URLs. Regex: ^[\w!@$()`.+,"\-']{3,64}$
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
        license: _projects.Project.License,
        project_type: str,
        additional_categories: list[str] | None = None,
        issues_url: str | None = None,
        source_url: str | None = None,
        wiki_url: str | None = None,
        discord_url: str | None = None,
        auth: str = "",
    ) -> None:
        self.slug = slug
        self.title = title
        self.description = description
        self.categories = categories
        self.client_side = client_side
        self.server_side = server_side
        self.body = body
        self.license = license._to_json()
        self.project_type = project_type
        self.additional_categories = additional_categories
        self.issues_url = issues_url
        self.source_url = source_url
        self.wiki_url = wiki_url
        self.discord_url = discord_url
        self.auth = auth
        self.donation_urls: list[dict]
        self.id: str
        self.downloads: int
        self.icon_url: str
        self.color: str
        self.team: str
        self.moderator_message: dict
        self.published: str
        self.updated: str
        self.approved: str
        self.followers: int
        self.status: str
        self.versions: list[str]
        self.game_versions: list[_literals.game_version_literal]
        self.loaders: list[_literals.loader_literal]
        self.gallery: list[dict]

    @staticmethod
    def _from_json(project_model_json: dict) -> ProjectModel:
        license = _projects.Project.License._from_json(
            project_model_json.get("license", ...)
        )
        result = ProjectModel(
            project_model_json.get("slug", ...),
            project_model_json.get("title", ...),
            project_model_json.get("description", ...),
            project_model_json.get("categories", ...),
            project_model_json.get("client_side", ...),
            project_model_json.get("server_side", ...),
            project_model_json.get("body", ...),
            license,
            project_model_json.get("project_type", ...),
            project_model_json.get("additional_categories"),
            project_model_json.get("issues_url"),
            project_model_json.get("source_url"),
            project_model_json.get("wiki_url"),
            project_model_json.get("discord_url"),
            project_model_json.get("authorization", ...),
        )
        result.id = project_model_json.get("id", ...)
        result.downloads = project_model_json.get("downloads", ...)
        result.donation_urls = project_model_json.get("donation_urls", ...)
        result.icon_url = project_model_json.get("icon_url", ...)
        result.color = project_model_json.get("color", ...)
        result.team = project_model_json.get("team", ...)
        result.moderator_message = project_model_json.get("moderator_message", ...)
        result.published = project_model_json.get("published", ...)
        result.updated = project_model_json.get("updated", ...)
        result.approved = project_model_json.get("approved", ...)
        result.followers = project_model_json.get("followers", ...)
        result.status = project_model_json.get("status", ...)
        result.versions = project_model_json.get("versions", ...)
        result.game_versions = project_model_json.get("game_versions", ...)
        result.loaders = project_model_json.get("loaders", ...)
        result.gallery = project_model_json.get("gallery", ...)
        return result


class _SearchResultModel(_Model):
    slug: str
    title: str
    description: str
    client_side: str
    server_side: str
    project_type: str
    downloads: int
    project_id: str
    author: str
    versions: list[str]
    follows: int
    date_created: object
    date_modified: object
    license: str
    categories: list[str]
    icon_url: str
    color: str
    display_categories: list[str]
    latest_version: list[str]
    gallery: list[str]
    featured_gallery: list[str]

    @staticmethod
    def _from_json(search_result_json: dict) -> _SearchResultModel:
        result = _SearchResultModel()
        result.slug = search_result_json.get("slug", ...)
        result.title = search_result_json.get("title", ...)
        result.description = search_result_json.get("description", ...)
        result.client_side = search_result_json.get("client_side", ...)
        result.server_side = search_result_json.get("server_side", ...)
        result.project_type = search_result_json.get("project_type", ...)
        result.downloads = search_result_json.get("downloads", ...)
        result.project_id = search_result_json.get("project_id", ...)
        result.author = search_result_json.get("author", ...)
        result.versions = search_result_json.get("versions", ...)
        result.follows = search_result_json.get("follows", ...)
        result.date_created = search_result_json.get("date_created")
        result.date_modified = search_result_json.get("date_modified")
        result.license = search_result_json.get("license", ...)
        result.categories = search_result_json.get("categories", ...)
        result.icon_url = search_result_json.get("icon_url", ...)
        result.color = search_result_json.get("color", ...)
        result.display_categories = search_result_json.get("display_categories", ...)
        result.latest_version = search_result_json.get("latest_version", ...)
        result.gallery = search_result_json.get("gallery", ...)
        result.featured_gallery = search_result_json.get("featured_gallery", ...)
        return result


class VersionModel(_Model):
    """The model used for the Version class.

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
        dependencies: list[_projects.Project.Dependency],
        game_versions: list[_literals.game_version_literal],
        version_type: _literals.version_type_literal,
        loaders: list[_literals.loader_literal],
        featured: bool,
        file_parts: list[str],
        changelog: str | None = None,
        status: _literals.version_status_literal | None = None,
        requested_status: _literals.requested_version_status_literal | None = None,
    ) -> None:
        self.name = name
        self.version_number = version_number
        self.changelog = changelog
        self.dependencies = _util.list_to_json(dependencies)
        self.game_versions = game_versions
        self.version_type = version_type
        self.loaders = loaders
        self.featured = featured
        self.status = status
        self.requested_status = requested_status
        self.file_parts = file_parts
        self.project_id: str
        self.id: str
        self.author_id: str
        self.date_published: object
        self.downloads: int

    @staticmethod
    def _from_json(version_json: dict) -> VersionModel:
        result = VersionModel(
            version_json.get("name", ...),
            version_json.get("version_number", ...),
            version_json.get("dependencies", ...),
            version_json.get("game_versions", ...),
            version_json.get("version_type", ...),
            version_json.get("loaders", ...),
            version_json.get("featured", ...),
            version_json.get("files", ...),
            version_json.get("changelog"),
            version_json.get("status"),
            version_json.get("requested_status"),
        )
        result.project_id = version_json.get("project_id", ...)
        result.id = version_json.get("id", ...)
        result.author_id = version_json.get("author_id", ...)
        result.date_published = version_json.get("date_published")
        result.downloads = version_json.get("downloads", ...)
        return result


class _UserModel(_Model):
    username: str
    id: str
    avatar_url: str
    created: str
    role: str
    name: str
    email: str
    bio: str
    payout_data: dict
    github_id: int
    badges: list[str]
    auth: str

    @staticmethod
    def _from_json(user_json: dict) -> _UserModel:
        result = _UserModel()
        result.username = user_json.get("username", ...)
        result.id = user_json.get("id", ...)
        result.avatar_url = user_json.get("avatar_url", ...)
        result.created = user_json.get("created", ...)
        result.role = user_json.get("role", ...)
        result.name = user_json.get("name", ...)
        result.email = user_json.get("email", ...)
        result.bio = user_json.get("bio", ...)
        result.payout_data = user_json.get("payout_data", ...)
        result.github_id = user_json.get("github_id", ...)
        result.badges = user_json.get("badges", ...)
        result.auth = user_json.get("authorization", "")
        return result
