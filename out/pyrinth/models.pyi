import pyrinth.literals as _literals
import pyrinth.projects as _projects
from _typeshed import Incomplete

class ProjectModel:
    slug: Incomplete
    title: Incomplete
    description: Incomplete
    categories: Incomplete
    client_side: Incomplete
    server_side: Incomplete
    body: Incomplete
    license: Incomplete
    project_type: Incomplete
    additional_categories: Incomplete
    issues_url: Incomplete
    source_url: Incomplete
    wiki_url: Incomplete
    discord_url: Incomplete
    auth: Incomplete
    donation_urls: Incomplete
    id_: Incomplete
    downloads: Incomplete
    icon_url: Incomplete
    color: Incomplete
    team: Incomplete
    moderator_message: Incomplete
    published: Incomplete
    updated: Incomplete
    approved: Incomplete
    followers: Incomplete
    status: Incomplete
    version_ids: Incomplete
    game_versions: Incomplete
    loaders: Incomplete
    gallery: Incomplete
    def __init__(self, slug: str, title: str, description: str, categories: list[str], client_side: str, server_side: str, body: str, license_: _projects.Project.License, project_type: str, additional_categories: list[str] | None = ..., issues_url: str | None = ..., source_url: str | None = ..., wiki_url: str | None = ..., discord_url: str | None = ..., auth: str = ...) -> None: ...

class _SearchResultModel:
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

class VersionModel:
    name: Incomplete
    version_number: Incomplete
    changelog: Incomplete
    dependencies: Incomplete
    game_versions: Incomplete
    version_type: Incomplete
    loaders: Incomplete
    featured: Incomplete
    status: Incomplete
    requested_status: Incomplete
    files: Incomplete
    project_id: Incomplete
    id: Incomplete
    author_id: Incomplete
    date_published: Incomplete
    downloads: Incomplete
    def __init__(self, name: str, version_number: str, dependencies: list['_projects.Project._Dependency'], game_versions: list[str], version_type: _literals.version_type_literal, loaders: list[str], featured: bool, file_parts: list[dict], changelog: str | None = ..., status: _literals.version_status_literal | None = ..., requested_status: _literals.requested_version_status_literal | None = ...) -> None: ...

class _UserModel:
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
