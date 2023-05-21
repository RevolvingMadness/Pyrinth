import pyrinth.literals as literals
import pyrinth.projects as projects
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
    donation_urls: Incomplete
    auth: Incomplete
    id: Incomplete
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
    def __init__(
        self,
        slug: str,
        title: str,
        description: str,
        categories: list[str],
        client_side: str,
        server_side: str,
        body: str,
        license_: projects.Project.License,
        project_type: str,
        additional_categories: list[str] | None = ...,
        issues_url: str | None = ...,
        source_url: str | None = ...,
        wiki_url: str | None = ...,
        discord_url: str | None = ...,
        auth: str | None = ...,
    ) -> None: ...

class SearchResultModel:
    slug: Incomplete
    title: Incomplete
    description: Incomplete
    client_side: Incomplete
    server_side: Incomplete
    project_type: Incomplete
    downloads: Incomplete
    project_id: Incomplete
    author: Incomplete
    versions: Incomplete
    follows: Incomplete
    date_created: Incomplete
    date_modified: Incomplete
    license: Incomplete
    categories: Incomplete
    icon_url: Incomplete
    color: Incomplete
    display_categories: Incomplete
    latest_version: Incomplete
    gallery: Incomplete
    featured_gallery: Incomplete
    def __init__(self) -> None: ...

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
        changelog: str | None = ...,
        status: literals.version_status_literal | None = ...,
        requested_status: literals.requested_version_status_literal | None = ...,
    ) -> None: ...

class UserModel:
    username: Incomplete
    id: Incomplete
    avatar_url: Incomplete
    created: Incomplete
    role: Incomplete
    name: Incomplete
    email: Incomplete
    bio: Incomplete
    payout_data: Incomplete
    github_id: Incomplete
    badges: Incomplete
    auth: Incomplete
    def __init__(self) -> None: ...
