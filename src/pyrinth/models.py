"""Contains all models used in Pyrinth."""

from typing import Optional
import json
from pyrinth.util import remove_null_values
from pyrinth.projects import Project


class ProjectModel:
    """The model used for the Project class."""

    def __init__(
        self, slug: str, title: str,
        description: str, categories: list[str],
        client_side: str, server_side: str, body: str,
        license_: 'Project.License', project_type: str,
        additional_categories: Optional[list[str]] = None,
        issues_url: Optional[str] = None, source_url: Optional[str] = None,
        wiki_url: Optional[str] = None, discord_url: Optional[str] = None,
        auth=None
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

    @staticmethod
    def from_json(json_: dict) -> 'ProjectModel':
        """Utility function."""
        license_ = Project.License.from_json(json_['license'])

        result = ProjectModel(
            json_['slug'], json_['title'], json_['description'],
            json_['categories'], json_['client_side'], json_['server_side'],
            json_['body'], license_, json_['project_type'],
            json_['additional_categories'], json_[
                'issues_url'], json_['source_url'],
            json_['wiki_url'], json_['discord_url'], json_['authorization']
        )
        result.id = json_['id']
        result.downloads = json_['downloads']
        result.donation_urls = json_['donation_urls']
        return result

    def to_json(self) -> dict:
        """Utility function."""
        result = {
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'categories': self.categories,
            'client_side': self.client_side,
            'server_side': self.server_side,
            'body': self.body,
            'license_id': self.license['id'],
            'project_type': self.project_type,
            'additional_categories': self.additional_categories,
            'issues_url': self.issues_url,
            'source_url': self.source_url,
            'wiki_url': self.wiki_url,
            'discord_url': self.discord_url,
            'donation_urls': self.donation_urls,
            'license_url': self.license['url'],
            'id': self.id,
            'authorization': self.auth,
            'is_draft': True,
            'initial_versions': []
        }
        result = remove_null_values(result)
        return result

    def to_bytes(self) -> bytes:
        """Utility function."""
        return json.dumps(self.to_json()).encode()


class SearchResultModel:
    """The model used for the SearchResult class."""

    def __init__(
        self, slug: str, title: str, description: str,
        client_side: str, server_side: str, project_type: str,
        downloads: int, project_id: str, author: str, versions: list[str],
        follows: int, date_created, date_modified, license_, categories: list[str],
        icon_url: None, color: None, display_categories: list[str],
        latest_version: str, gallery: list[str], featured_gallery: None
    ) -> None:
        self.slug = slug
        self.title = title
        self.description = description
        self.client_side = client_side
        self.server_side = server_side
        self.project_type = project_type
        self.downloads = downloads
        self.project_id = project_id
        self.author = author
        self.versions = versions
        self.follows = follows
        self.date_created = date_created
        self.date_modified = date_modified
        self.license = license_
        self.categories = categories
        self.icon_url = icon_url
        self.color = color
        self.display_categories = display_categories
        self.latest_version = latest_version
        self.gallery = gallery
        self.featured_gallery = featured_gallery

    @staticmethod
    def from_json(json_: dict) -> 'SearchResultModel':
        """Utility function."""
        result = SearchResultModel(
            json_['slug'], json_['title'], json_['description'],
            json_['client_side'], json_['server_side'], json_['project_type'],
            json_['downloads'], json_['project_id'], json_['author'],
            json_['versions'], json_['follows'], json_['date_created'],
            json_['date_modified'], json_['license'], json_['categories'],
            json_['icon_url'], json_['color'], json_['display_categories'],
            json_['latest_version'], json_['gallery'],
            json_['featured_gallery']
        )

        return result

    def to_json(self) -> dict:
        """Utility function."""
        result = {
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'client_side': self.client_side,
            'server_side': self.server_side,
            'project_type': self.project_type,
            'downloads': self.downloads,
            'project_id': self.project_id,
            'author': self.author,
            'versions': self.versions,
            'follows': self.follows,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'license': self.license,
            'categories': self.categories,
            'icon_url': self.icon_url,
            'color': self.color,
            'display_categories': self.display_categories,
            'latest_version': self.latest_version,
            'gallery': self.gallery,
            'featured_gallery': self.featured_gallery
        }
        result = remove_null_values(result)
        return result

    def to_bytes(self) -> bytes:
        """Utility function."""
        return json.dumps(self.to_json()).encode()


class VersionModel:
    """The model used for the Version class."""

    def __init__(
        self, name: str, version_number: str, dependencies: list['Project.Dependency'],
        game_versions: list[str], version_type: str, loaders: list[str], featured: bool,
        file_parts: list[str], changelog: Optional[str] = None, status: Optional[str] = None,
        requested_status: Optional[str] = None
    ) -> None:
        from pyrinth.util import list_to_json
        self.name = name
        self.version_number = version_number
        self.changelog = changelog
        self.dependencies = list_to_json(dependencies)
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
    def from_json(json_: dict) -> 'VersionModel':
        """Utility function."""
        result = VersionModel(
            json_['name'], json_['version_number'], json_['dependencies'],
            json_['game_versions'], json_['version_type'], json_['loaders'],
            json_['featured'], json_['files'], json_['changelog'],
            json_['status'], json_['requested_status']
        )
        result.project_id = json_['project_id']
        result.id = json_['id']
        result.author_id = json_['author_id']
        result.date_published = json_['date_published']
        result.downloads = json_['downloads']
        return result

    def to_json(self) -> dict:
        """Utility function."""
        result = {
            'name': self.name,
            'version_number': self.version_number,
            'changelog': self.changelog,
            'dependencies': self.dependencies,
            'game_versions': self.game_versions,
            'version_type': self.version_type,
            'loaders': self.loaders,
            'featured': self.featured,
            'status': self.status,
            'requested_status': self.requested_status,
            'file_parts': self.files,
            'project_id': self.project_id,
            'id': self.id,
            'author_id': self.author_id,
            'date_published': self.date_published,
            'downloads': self.downloads
        }
        result = remove_null_values(result)
        return result

    def to_bytes(self) -> bytes:
        """Utility function."""
        return json.dumps(self.to_json()).encode()


class UserModel:
    """The model used for the User class."""

    def __init__(
        self, username: str, id_: str, avatar_url: str,
        created, role: str, name: Optional[str] = None,
        email: Optional[str] = None, bio: Optional[str] = None,
        payout_data=None, github_id: Optional[str] = None,
        badges: Optional[int] = None, auth=None
    ) -> None:
        self.username = username
        self.id = id_
        self.avatar_url = avatar_url
        self.created = created
        self.role = role
        self.name = name
        self.email = email
        self.bio = bio
        self.payout_data = payout_data
        self.github_id = github_id
        self.badges = badges
        self.auth = auth

    @staticmethod
    def from_json(json_: dict) -> 'UserModel':
        """Utility function."""
        result = UserModel(
            json_['username'], json_['id'], json_['avatar_url'],
            json_['created'], json_['role'], json_['name'],
            json_['email'], json_['bio'], json_['payout_data'],
            json_['github_id'], json_['badges'], json_['authorization']
        )
        return result

    def to_json(self) -> dict:
        """Utility function."""
        result = {
            'username': self.username,
            'id': self.id,
            'avatar_url': self.avatar_url,
            'created': self.created,
            'role': self.role,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'payout_data': self.payout_data,
            'github_id': self.github_id,
            'badges': self.badges,
            'authorization': self.auth
        }
        result = remove_null_values(result)
        return result

    def to_bytes(self) -> bytes:
        """Utility function."""
        return json.dumps(self.to_json()).encode()
