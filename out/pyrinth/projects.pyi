import datetime as dt
import pyrinth.literals as literals
import pyrinth.models as models
import pyrinth.teams as teams
import typing
import pyrinth.users as users
from _typeshed import Incomplete

class Project:
    model: Incomplete
    def __init__(self, project_model: models.ProjectModel) -> None: ...
    @property
    def donations(self) -> list["Project.Donation"]: ...
    @staticmethod
    def get(id_: str, authorization: str = ...) -> Project: ...
    @staticmethod
    def get_multiple(ids: list[str]) -> list["Project"]: ...
    def get_latest_version(
        self,
        loaders: list[str] | None = ...,
        game_versions: list[str] | None = ...,
        featured: bool | None = ...,
        types: literals.version_type_literal | None = ...,
        auth: str | None = ...,
    ) -> Project.Version: ...
    @property
    def gallery(self) -> list["Project.GalleryImage"]: ...
    def is_client_side(self) -> bool: ...
    def is_server_side(self) -> bool: ...
    @property
    def downloads(self) -> int: ...
    @property
    def categories(self) -> list[str]: ...
    @property
    def additional_categories(self) -> list[str]: ...
    @property
    def all_categories(self) -> list[str]: ...
    @property
    def license(self) -> Project.License: ...
    def get_specific_version(
        self, semantic_version: str
    ) -> typing.Optional["Project.Version"]: ...
    def download(self, recursive: bool = ...) -> None: ...
    def get_versions(
        self,
        loaders: list[str] | None = ...,
        game_versions: list[str] | None = ...,
        featured: bool | None = ...,
        types: literals.version_type_literal | None = ...,
        auth: str | None = ...,
    ) -> list["Project.Version"]: ...
    def get_oldest_version(
        self,
        loaders: list[str] | None = ...,
        game_versions: list[str] | None = ...,
        featured: bool | None = ...,
        types: literals.version_type_literal | None = ...,
        auth: str | None = ...,
    ) -> Project.Version: ...
    @property
    def id(self) -> str: ...
    @property
    def slug(self) -> str: ...
    @property
    def name(self) -> str: ...
    @staticmethod
    def get_version(id_: str) -> Project.Version: ...
    def create_version(self, version_model, auth: str | None = ...) -> int: ...
    def change_icon(self, file_path: str, auth: str | None = ...) -> bool: ...
    def delete_icon(self, auth: str | None = ...) -> bool: ...
    def add_gallery_image(
        self, image: Project.GalleryImage, auth: str | None = ...
    ) -> bool: ...
    def modify_gallery_image(
        self,
        url: str,
        featured: bool | None = ...,
        title: str | None = ...,
        description: str | None = ...,
        ordering: int | None = ...,
        auth: str | None = ...,
    ) -> bool: ...
    def delete_gallery_image(self, url: str, auth: str | None = ...) -> bool: ...
    def modify(
        self,
        slug: str | None = ...,
        title: str | None = ...,
        description: str | None = ...,
        categories: list[str] | None = ...,
        client_side: str | None = ...,
        server_side: str | None = ...,
        body: str | None = ...,
        additional_categories: list[str] | None = ...,
        issues_url: str | None = ...,
        source_url: str | None = ...,
        wiki_url: str | None = ...,
        discord_url: str | None = ...,
        license_id: str | None = ...,
        license_url: str | None = ...,
        status: literals.project_status_literal | None = ...,
        requested_status: literals.requested_project_status_literal | None = ...,
        moderation_message: str | None = ...,
        moderation_message_body: str | None = ...,
        auth: str | None = ...,
    ) -> bool: ...
    def delete(self, auth: str | None = ...) -> typing.Literal[True]: ...
    @property
    def dependencies(self) -> list["Project"]: ...
    @staticmethod
    def search(
        query: str = ...,
        facets: list[list[str]] | None = ...,
        index: literals.index_literal = ...,
        offset: int = ...,
        limit: int = ...,
        filters: list[str] | None = ...,
    ) -> list["Project.SearchResult"]: ...
    @property
    def team_members(self) -> list[teams.Team.TeamMember]: ...
    @property
    def team(self) -> teams.Team: ...

    class Version:
        model: Incomplete
        def __init__(self, version_model: models.VersionModel) -> None: ...
        @property
        def type(self) -> str: ...
        @property
        def dependencies(self) -> list["Project.Dependency"]: ...
        @staticmethod
        def get(id_: str) -> Project.Version: ...
        @staticmethod
        def get_from_hash(
            hash_: str,
            algorithm: literals.sha_algorithm_literal = ...,
            multiple: bool = ...,
        ) -> typing.Union["Project.Version", list["Project.Version"]]: ...
        @staticmethod
        def delete_file_from_hash(
            auth: str,
            hash_: str,
            version_id: str,
            algorithm: literals.sha_algorithm_literal = ...,
        ) -> typing.Literal[True]: ...
        @property
        def files(self) -> list["Project.File"]: ...
        def download(self, recursive: bool = ...) -> None: ...
        @property
        def project(self) -> Project: ...
        @property
        def primary_files(self) -> list["Project.File"]: ...
        @property
        def author(self) -> users.User: ...
        def is_featured(self) -> bool: ...
        @property
        def date_published(self) -> dt.datetime: ...
        @property
        def downloads(self) -> int: ...
        @property
        def name(self) -> str: ...
        @property
        def version_number(self) -> str: ...

    class GalleryImage:
        file_path: Incomplete
        ext: Incomplete
        featured: Incomplete
        title: Incomplete
        description: Incomplete
        ordering: Incomplete
        def __init__(
            self,
            file_path: str,
            featured: bool,
            title: str,
            description: str,
            ordering: int = ...,
        ) -> None: ...

    class File:
        hashes: Incomplete
        url: Incomplete
        name: Incomplete
        primary: Incomplete
        size: Incomplete
        file_type: Incomplete
        extension: Incomplete
        def __init__(
            self,
            hashes: dict[str, str],
            url: str,
            filename: str,
            primary: str,
            size: int,
            file_type: str,
        ) -> None: ...
        def is_resourcepack(self) -> bool: ...

    class License:
        id: Incomplete
        name: Incomplete
        url: Incomplete
        def __init__(self, id_: str, name: str, url: str | None = ...) -> None: ...

    class Donation:
        id: Incomplete
        platform: Incomplete
        url: Incomplete
        def __init__(self, id_: str, platform: str, url: str) -> None: ...

    class Dependency:
        dependency_option: Incomplete
        file_name: Incomplete
        version_id: Incomplete
        project_id: Incomplete
        def __init__(self) -> None: ...
        @property
        def version(self) -> Project.Version: ...
        def is_required(self) -> bool: ...
        def is_optional(self) -> bool: ...
        def is_incompatible(self) -> bool: ...

    class SearchResult:
        model: Incomplete
        def __init__(self, search_result_model: models.SearchResultModel) -> None: ...
