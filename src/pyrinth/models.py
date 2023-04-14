"""Contains all models used in Pyrinth."""

import json
import typing

import pyrinth.literals as literals
import pyrinth.projects as projects
import pyrinth.util as util


class ProjectModel:
    """The model used for the Project class."""

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
        additional_categories: typing.Optional[list[str]] = None,
        issues_url: typing.Optional[str] = None,
        source_url: typing.Optional[str] = None,
        wiki_url: typing.Optional[str] = None,
        discord_url: typing.Optional[str] = None,
        auth=None,
    ) -> None:
        self.slug = slug
        self.title = title
        self.description = description
        self.categories = categories
        self.client_side = client_side
        self.server_side = server_side
        self.body = body
        self.license = license_.to_json()
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
    def from_json(json_: dict) -> "ProjectModel":
        """Utility function."""
        license_ = projects.Project.License.from_json(json_.get("license"))  # type: ignore

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

    def to_json(self) -> dict:
        """Utility function."""
        result = {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "categories": self.categories,
            "client_side": self.client_side,
            "server_side": self.server_side,
            "body": self.body,
            "license_id": self.license.get("id"),
            "project_type": self.project_type,
            "additional_categories": self.additional_categories,
            "issues_url": self.issues_url,
            "source_url": self.source_url,
            "wiki_url": self.wiki_url,
            "discord_url": self.discord_url,
            "donation_urls": self.donation_urls,
            "license_url": self.license.get("url"),
            "id": self.id,
            "authorization": self.auth,
            "is_draft": True,
            "initial_versions": [],
        }
        result = util.remove_null_values(result)
        return result

    def to_bytes(self) -> bytes:
        """Utility function."""
        return json.dumps(self.to_json()).encode()


class SearchResultModel:
    """The model used for the SearchResult class."""

    def __init__(self) -> None:
        self.slug: typing.Optional[str] = None
        self.title: typing.Optional[str] = None
        self.description: typing.Optional[str] = None
        self.client_side: typing.Optional[str] = None
        self.server_side: typing.Optional[str] = None
        self.project_type: typing.Optional[str] = None
        self.downloads: typing.Optional[int] = None
        self.project_id: typing.Optional[str] = None
        self.author = None
        self.versions: typing.Optional[list[str]] = None
        self.follows: typing.Optional[int] = None
        self.date_created = None
        self.date_modified = None
        self.license: typing.Optional["projects.Project.License"] = None
        self.categories: typing.Optional[list[str]] = None
        self.icon_url: typing.Optional[str] = None
        self.color: typing.Optional[str] = None
        self.display_categories: typing.Optional[list] = None
        self.latest_version = None
        self.gallery = None
        self.featured_gallery = None

    @staticmethod
    def from_json(json_: dict) -> "SearchResultModel":
        """Utility function."""
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

    def to_json(self) -> dict:
        """Utility function."""
        result = {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "client_side": self.client_side,
            "server_side": self.server_side,
            "project_type": self.project_type,
            "downloads": self.downloads,
            "project_id": self.project_id,
            "author": self.author,
            "versions": self.versions,
            "follows": self.follows,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "license": self.license,
            "categories": self.categories,
            "icon_url": self.icon_url,
            "color": self.color,
            "display_categories": self.display_categories,
            "latest_version": self.latest_version,
            "gallery": self.gallery,
            "featured_gallery": self.featured_gallery,
        }
        result = util.remove_null_values(result)
        return result

    def to_bytes(self) -> bytes:
        """Utility function."""
        return json.dumps(self.to_json()).encode()


class VersionModel:
    """The model used for the Version class."""

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
        changelog: typing.Optional[str] = None,
        status: typing.Optional[literals.version_status_literal] = None,
        requested_status: typing.Optional[
            literals.requested_version_status_literal
        ] = None,
    ) -> None:
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
    def from_json(json_: dict) -> "VersionModel":
        """Utility function."""
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

    def to_json(self) -> dict:
        """Utility function."""
        result = {
            "name": self.name,
            "version_number": self.version_number,
            "changelog": self.changelog,
            "dependencies": self.dependencies,
            "game_versions": self.game_versions,
            "version_type": self.version_type,
            "loaders": self.loaders,
            "featured": self.featured,
            "status": self.status,
            "requested_status": self.requested_status,
            "file_parts": self.files,
            "project_id": self.project_id,
            "id": self.id,
            "author_id": self.author_id,
            "date_published": self.date_published,
            "downloads": self.downloads,
        }
        result = util.remove_null_values(result)
        return result

    def to_bytes(self) -> bytes:
        """Utility function."""
        return json.dumps(self.to_json()).encode()


class UserModel:
    """The model used for the User class."""

    def __init__(self) -> None:
        self.username: typing.Optional[str] = None
        self.id: typing.Optional[str] = None
        self.avatar_url: typing.Optional[str] = None
        self.created = None
        self.role: typing.Optional[str] = None
        self.name: typing.Optional[str] = None
        self.email: typing.Optional[str] = None
        self.bio: typing.Optional[str] = None
        self.payout_data = None
        self.github_id: typing.Optional[int] = None
        self.badges: typing.Optional[list[str]] = None
        self.auth: typing.Optional[str] = None

    @staticmethod
    def from_json(json_: dict) -> "UserModel":
        """Utility function."""
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

    def to_json(self) -> dict:
        """Utility function."""
        result = {
            "username": self.username,
            "id": self.id,
            "avatar_url": self.avatar_url,
            "created": self.created,
            "role": self.role,
            "name": self.name,
            "email": self.email,
            "bio": self.bio,
            "payout_data": self.payout_data,
            "github_id": self.github_id,
            "badges": self.badges,
            "authorization": self.auth,
        }
        result = util.remove_null_values(result)
        return result

    def to_bytes(self) -> bytes:
        """Utility function."""
        return json.dumps(self.to_json()).encode()
