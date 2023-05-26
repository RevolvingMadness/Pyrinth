"""Project can be mods or modpacks and are created by users."""
from __future__ import annotations

import dataclasses
import datetime as _datetime
import json as _json

import requests as _requests

import pyrinth.exceptions as _exceptions
import pyrinth.literals as _literals
import pyrinth.models as _models
import pyrinth.teams as _teams
import pyrinth.users as _users
import pyrinth.util as _util


class Project:
    """Project can be mods or modpacks and are created by users.

    Attributes:
        model (ProjectModel): The project's model
    """

    def __init__(self, project_model: _models.ProjectModel) -> None:
        self.project_model = project_model

    @property
    def donations(self) -> list[Project.Donation]:
        return _util.list_to_object(Project.Donation, self.project_model.donation_urls)

    def _get_auth(self, auth: str | None) -> str:
        if auth:
            return auth
        return self.project_model.auth

    @staticmethod
    def get(id_: str, authorization: str = "") -> Project:
        """Get a project by ID or slug.

        Args:
            id_ (str): The ID or slug of the project
            auth (str, optional): An optional authorization token when getting the project

        Raises:
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (Project): The project that was found
        """
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/project/{id_}",
            headers={"authorization": authorization},
            timeout=60,
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        response.update({"authorization": authorization})
        return Project(_models.ProjectModel._from_json(response))

    @staticmethod
    def get_multiple(ids: list[str]) -> list[Project]:
        """Get multiple projects.

        Args:
            ids (list[str]): The IDs of the projects

        Raises:
            InvalidRequestError: Invalid request

        Returns:
            (list[Project]): The projects that were found
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/projects",
            params={"ids": _json.dumps(ids)},
            timeout=60,
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return [
            Project(_models.ProjectModel._from_json(project_json))
            for project_json in response
        ]

    def get_latest_version(
        self,
        loaders: list[_literals.loader_literal] | None = None,
        game_versions: list[_literals.game_version_literal] | None = None,
        featured: bool | None = None,
        types: _literals.version_type_literal | None = None,
        auth: str | None = None,
    ) -> Project.Version | None:
        """Get the projects latest version.

        Args:
            loaders (list[str], optional): The loaders filter. Defaults to None
            game_versions (list[str], optional): The game versions filter. Defaults to None
            featured (bool, optional): The is featured filter. Defaults to None
            types (Literal["release", "beta", "alpha"], optional): The types filter. Defaults to None
            auth (str, optional): The authorization token. Defaults to None

        Returns:
            (Project.Version): The project's latest version
        """
        versions = self.get_versions(loaders, game_versions, featured, types, auth)
        if len(versions) == 0:
            return None
        return versions[0]

    @property
    def gallery(self) -> list[Project.GalleryImage]:
        return _util.list_to_object(Project.GalleryImage, self.project_model.gallery)

    @property
    def description(self) -> str:
        return self.project_model.description

    @property
    def body(self) -> str:
        return self.project_model.body

    def is_client_side(self) -> bool:
        """Check if this project is client side.

        Returns:
            (bool): Whether this project is client side
        """
        return True if self.project_model.client_side == "required" else False

    def is_server_side(self) -> bool:
        """Check if this project is server side.

        Returns:
            (bool): Whether this project is server side
        """
        return True if self.project_model.server_side == "required" else False

    @property
    def downloads(self) -> int:
        return self.project_model.downloads

    @property
    def categories(self) -> list[str]:
        return self.project_model.categories

    @property
    def additional_categories(self) -> list[str] | None:
        return self.project_model.additional_categories

    @property
    def all_categories(self) -> list[str]:
        if self.additional_categories is None:
            return self.categories

        return self.categories + self.additional_categories

    @property
    def license(self) -> Project.License:
        return Project.License._from_json(self.project_model.license)

    def get_specific_version(self, semantic_version: str) -> Project.Version | None:
        """Get a specific version based on the semantic version.

        Args:
            semantic_version (str): The semantic version to search for

        Returns:
            (Project.Version): The version that was found using the semantic version
            (None): No version was found with that semantic version
        """
        versions = self.get_versions()
        if versions:
            for version in versions:
                if version.version_model.version_number == semantic_version:
                    return version
        return None

    def download(self, recursive: bool = False) -> int:
        """Download the project.

        Args:
            recursive (bool): Whether to download dependencies. Defaults to False
        """
        latest = self.get_latest_version()
        if latest is None:
            return 0
        files = latest.files
        for file in files:
            file_content = _requests.get(file.url, timeout=60).content
            open(file.name, "wb").write(file_content)
        if recursive:
            dependencies = latest.dependencies
            for dep in dependencies:
                files = dep.version.files
                for file in files:
                    file_content = _requests.get(file.url, timeout=60).content
                    open(file.name, "wb").write(file_content)
        return 1

    def get_versions(
        self,
        loaders: list[_literals.loader_literal] | None = None,
        game_versions: list[_literals.game_version_literal] | None = None,
        featured: bool | None = None,
        types: _literals.version_type_literal | None = None,
        auth: str | None = None,
    ) -> list[Project.Version]:
        """Get project versions based on filters.

        Args:
            loaders (list[str], optional): The types of loaders to filter for
            game_versions (list[str], optional): The game versions to filter for
            featured (bool, optional): Allows to filter for featured or non-featured versions only
            types (Literal["release", "beta", "alpha"], optional): The release type of version
            auth (str, optional): An optional authorization token to use when getting the project versions

        Raises:
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (list[Project.Version]): The versions that were found
        """
        filters = {
            "loaders": loaders,
            "game_versions": game_versions,
            "featured": featured,
        }
        filters = _util.remove_null_values(filters)
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}/version",
            params=_util.json_to_query_params(filters),
            headers={"authorization": self._get_auth(auth)},
            timeout=60,
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        versions = [
            self.Version(_models.VersionModel._from_json(version))
            for version in response
        ]
        if not types:
            return versions
        result = []
        for version in versions:
            if version.version_model.version_type in types:
                result.append(version)
        return result

    def get_oldest_version(
        self,
        loaders: list[_literals.loader_literal] | None = None,
        game_versions: list[_literals.game_version_literal] | None = None,
        featured: bool | None = None,
        type: _literals.version_type_literal | None = None,
        auth: str | None = None,
    ) -> Project.Version | None:
        """Get the oldest project version.

        Args:
            loaders (list[str], optional): The types of loaders to filter for
            game_versions (list[str], optional): The game versions to filter for
            featured (bool, optional): Allows to filter for featured or non-featured versions only
            types (Literal["release", "beta", "alpha"], optional): The type of version
            auth (str, optional): An optional authorization token to use when getting the project versions

        Returns:
            (Project.Version): The version that was found
        """
        versions = self.get_versions(loaders, game_versions, featured, type, auth)
        if len(versions) == 0:
            return None
        return versions[-1]

    @property
    def id(self) -> str:
        return self.project_model.id

    @property
    def issues_url(self) -> str | None:
        return self.project_model.issues_url

    @property
    def source_url(self) -> str | None:
        return self.project_model.source_url

    @property
    def wiki_url(self) -> str | None:
        return self.project_model.wiki_url

    @property
    def discord_url(self) -> str | None:
        return self.project_model.discord_url

    @property
    def slug(self) -> str:
        return self.project_model.slug

    @property
    def name(self) -> str:
        return self.project_model.title

    @staticmethod
    def get_version(id_: str) -> Project.Version:
        """Get a version by ID.

        Args:
            id_ (str): The ID of the version

        Raises:
            NotFoundError: The requested version wasn't found or no authorization to see this version
            InvalidRequestError: Invalid request

        Returns:
            (Project.Version): The version that was found
        """
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/version/{id_}", timeout=60
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested version wasn't found or no authorization to see this version"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return Project.Version(_models.VersionModel._from_json(response))

    def create_version(
        self, version_model: _models.VersionModel, auth: str | None = None
    ) -> int:
        """Create a new version on the project.

        Args:
            auth (str, optional): The authorization token to use when creating the version
            version_model (VersionModel): The model to use when creating the version

        Raises:
            NoAuthorizationError: No authorization to create this version
            InvalidRequestError: Invalid request

        Returns:
            (int): Whether creating the version was successful
        """
        version_model.project_id = self.id

        files = {}

        for file in version_model.file_parts:
            files[file] = open(file, "rb")

        raw_response = _requests.post(
            "https://api.modrinth.com/v2/version",
            headers={"authorization": self._get_auth(auth)},
            data={"data": _json.dumps(version_model._to_json())},
            files=files,
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to create this version"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    def change_icon(self, file_path: str, auth: str | None = None) -> bool:
        """Change the project icon.

        Args:
            file_path (str): The file path of the image to use for the new project icon
            auth (str, optional): The authorization token to use when changing the project icon

        Raises:
            InvalidParamError: Invalid input for new icon
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the project icon change was successful
        """
        raw_response = _requests.patch(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}/icon",
            params={"ext": file_path.split(".")[-1]},
            headers={"authorization": self._get_auth(auth)},
            data=open(file_path, "rb"),
            timeout=60,
        )
        match raw_response.status_code:
            case 400:
                raise _exceptions.InvalidParamError("Invalid input for new icon")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    def delete_icon(self, auth: str | None = None) -> bool:
        """Delete the project icon.

        Args:
            auth (str, optional): The authorization token to use when deleting the project icon

        Raises:
            InvalidParamError: Invalid input
            NoAuthorizationError: No authorization to edit this project
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the project icon deletion was successful
        """
        raw_response = _requests.delete(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}/icon",
            headers={"authorization": self._get_auth(auth)},
            timeout=60,
        )
        match raw_response.status_code:
            case 400:
                raise _exceptions.InvalidParamError("Invalid input")
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to edit this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    def add_gallery_image(
        self, image: Project.GalleryImage, auth: str | None = None
    ) -> bool:
        """Add a gallery image to the project.

        Args:
            image (Project.GalleryImage): The gallery image to add
            auth (str, optional): The authorization token to use when adding the gallery image

        Raises:
            NoAuthorizationError: No authorization to create a gallery image
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (bool): If the gallery image addition was successful
        """
        raw_response = _requests.post(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery",
            headers={"authorization": self._get_auth(auth)},
            params=image._to_json(),
            data=open(image.file_path, "rb"),
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to create a gallery image"
                )
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    def modify_gallery_image(
        self,
        url: str,
        featured: bool | None = None,
        title: str | None = None,
        description: str | None = None,
        ordering: int | None = None,
        auth: str | None = None,
    ) -> bool:
        """Modify a gallery image.

        Args:
            url (str): URL link of the image to modify
            featured (bool, optional): Whether the image is featured
            title (str, optional): New title of the image
            description (str, optional): New description of the image
            ordering (int, optional): New ordering of the image
            auth (str, optional): Authentication token when modifying the gallery image

        Raises:
            NoAuthorizationError: No authorization to edit this gallery image
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the gallery image modification was successful
        """
        modified_json = {
            "url": url,
            "featured": featured,
            "title": title,
            "description": description,
            "ordering": ordering,
        }
        modified_json = _util.remove_null_values(modified_json)
        raw_response = _requests.patch(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery",
            params=modified_json,
            headers={"authorization": self._get_auth(auth)},
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to edit this gallery image"
                )
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    def delete_gallery_image(self, url: str, auth: str | None = None) -> bool:
        """Delete a gallery image.

        Args:
            url (str): URL link of the image to delete
            auth (str, optional): Authentication token to use when deleting the gallery image

        Raises:
            InvalidParamError: Invalid URL or project specified
            NoAuthorizationError: No authorization to delete this gallery image
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the gallery image deletion was successful
        """
        if "-raw" in url:
            raise _exceptions.InvalidParamError(
                "Please use cdn.modrinth.com instead of cdn-raw.modrinth.com"
            )
        raw_response = _requests.delete(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery",
            headers={"authorization": self._get_auth(auth)},
            params={"url": url},
            timeout=60,
        )
        match raw_response.status_code:
            case 400:
                raise _exceptions.InvalidParamError("Invalid URL or project specified")
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to delete this gallery image"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    def modify(
        self,
        slug: str | None = None,
        title: str | None = None,
        description: str | None = None,
        categories: list[str] | None = None,
        client_side: str | None = None,
        server_side: str | None = None,
        body: str | None = None,
        additional_categories: list[str] | None = None,
        issues_url: str | None = None,
        source_url: str | None = None,
        wiki_url: str | None = None,
        discord_url: str | None = None,
        license_id: str | None = None,
        license_url: str | None = None,
        status: _literals.project_status_literal | None = None,
        requested_status: _literals.requested_project_status_literal | None = None,
        moderation_message: str | None = None,
        moderation_message_body: str | None = None,
        auth: str | None = None,
    ) -> bool:
        r"""Modify the project.

        Args:
            slug (str, optional): The slug of a project, used for vanity URLs. Regex: ^[\w!@$()`.+,"\-']{3,64}$
            title (str, optional): The title or name of the project
            description (str, optional): A short description of the project
            categories (list[str], optional): A list of categories that the project has
            client_side (str, optional): The client side support of the project
            server_side (str, optional): The server side support of the project
            body (str, optional): A long form description of the project
            additional_categories (list[str], optional): A list of categories which are searchable but non-primary
            issues_url (str, optional): An optional link to where to submit bugs or issues with the project
            source_url (str, optional): An optional link to the source code of the project
            wiki_url (str, optional): An optional link to the project's wiki page or other relevant information
            discord_url (str, optional): An optional invite link to the project's discord
            license_id (str, optional): The SPDX license ID of a project
            license_url (str, optional): The URL to this license
            status (Literal["approved", "archived", "rejected", "draft", "unlisted", "processing", "withheld", "scheduled", "private", "unknown"], optional): The status of the project
            requested_status (Literal["approved", "archived", "unlisted", "private", "draft"], optional): The requested status when submitting for review or scheduling the project for release
            moderation_message (str, optional): The title of the moderators' message for the project
            moderation_message_body (str, optional): The body of the moderators' message for the project
            auth (str, optional): Authentication token to use when modifying the project

        Raises:
            InvalidParamError: Please specify at least 1 optional argument
            NoAuthorizationError: No authorization to modify this project
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the project modification was successful
        """
        modified_json = {
            "slug": slug,
            "title": title,
            "description": description,
            "categories": categories,
            "client_side": client_side,
            "server_side": server_side,
            "body": body,
            "additional_categories": additional_categories,
            "issues_url": issues_url,
            "source_url": source_url,
            "wiki_url": wiki_url,
            "discord_url": discord_url,
            "license_id": license_id,
            "license_url": license_url,
            "status": status,
            "requested_status": requested_status,
            "moderation_message": moderation_message,
            "moderation_message_body": moderation_message_body,
        }
        modified_json = _util.remove_null_values(modified_json)
        if not modified_json:
            raise _exceptions.InvalidParamError(
                "Please specify at least 1 optional argument"
            )
        raw_response = _requests.patch(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}",
            data=_json.dumps(modified_json),
            headers={
                "Content-Type": "application/json",
                "authorization": self._get_auth(auth),
            },
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to edit this project"
                )
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    @property
    def followers(self) -> int:
        return self.project_model.followers

    def delete(self, auth: str | None = None) -> bool:
        """Delete the project.

        Args:
            auth (str, optional): Authentication token to use when deleting the project

        Raises:
            NotFoundError: The requested project wasn't found
            NoAuthorizationError: No authorization to delete this project
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the project deletion was successful
        """
        raw_response = _requests.delete(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}",
            headers={"authorization": self._get_auth(auth)},
            timeout=60,
        )
        match raw_response.status_code:
            case 400:
                raise _exceptions.NotFoundError("The requested project was not found")
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to delete this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    @property
    def dependencies(self) -> list[Project]:
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/project/{self.project_model.slug}/dependencies",
            timeout=60,
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return [
            Project(_models.ProjectModel._from_json(dependency_json))
            for dependency_json in response.get("projects", ...)
        ]

    @staticmethod
    def search(
        query: str = "",
        facets: list[list[str]] | None = None,
        index: _literals.index_literal = "relevance",
        offset: int = 0,
        limit: int = 10,
        filters: list[str] | None = None,
    ) -> list[Project._SearchResult]:
        """Search for projects.

        Args:
            query (str, optional): The query to search for
            facets (list[list[str]], optional): The recommended way of filtering search results. [Learn more about using facets](https://docs.modrinth.com/docs/tutorials/api_search)
            index (Literal["relevance", "downloads", "follows", "newest", "updated"], optional): The sorting method used for sorting search results
            offset (int, optional): The offset into the search. Skip this number of results
            limit (int, optional): The number of results returned by the search
            filters (list[str], optional): A list of filters relating to the properties of a project. Use filters when there isn't an available facet for your needs. [More information](https://docs.meilisearch.com/reference/features/filtering.html)

        Raises:
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (list[Project.SearchResult]): The project search results
        """
        params = {}
        if query != "":
            params.update({"query": query})
        if facets:
            params.update({"facets": _json.dumps(facets)})
        if index != "relevance":
            params.update({"index": index})
        if offset != 0:
            params.update({"offset": str(offset)})
        if limit != 10:
            params.update({"limit": str(limit)})
        if filters:
            params.update({"filters": _json.dumps(filters)})
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/search", params=params, timeout=60
        )
        response: dict = raw_response.json()
        return [
            Project._SearchResult(_models._SearchResultModel._from_json(project))
            for project in response.get("hits", ...)
        ]

    @property
    def team_members(self) -> list[_teams._Team._TeamMember]:
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/project/{self.project_model.id}/members",
            timeout=60,
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return [
            _teams._Team._TeamMember._from_json(team_member) for team_member in response
        ]

    @property
    def team(self) -> _teams._Team:
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/project/{self.project_model.id}/members",
            timeout=60,
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return _teams._Team._from_json(response)

    def __repr__(self) -> str:
        return f"Project: {self.project_model.title}"

    class Version:
        """Versions contain download links to files with additional metadata.

        Attributes:
            model (VersionModel): The version model associated with the version

        """

        def __init__(self, version_model: _models.VersionModel) -> None:
            self.version_model = version_model

        @property
        def type(self) -> str:
            return self.version_model.version_type

        @property
        def dependencies(self) -> list[Project.Dependency]:
            return [
                Project.Dependency._from_json(dependency_json)  # type: ignore
                for dependency_json in self.version_model.dependencies
            ]

        @staticmethod
        def get(id_: str) -> Project.Version:
            """Get a version by ID.

            Args:
                id_ (str): The ID of the version

            Raises:
                NotFoundError: The requested version wasn't found or no authorization to see this version
                InvalidRequestError: Invalid request

            Returns:
                (Project.Version): The version that was found
            """
            raw_response = _requests.get(
                f"https://api.modrinth.com/v2/version/{id_}", timeout=60
            )
            match raw_response.status_code:
                case 404:
                    raise _exceptions.NotFoundError(
                        "The requested version wasn't found or no authorization to see this version"
                    )
            if not raw_response.ok:
                raise _exceptions.InvalidRequestError(raw_response.text)
            response: dict = raw_response.json()
            return Project.Version(_models.VersionModel._from_json(response))

        @staticmethod
        def get_from_hash(
            hash_: str,
            algorithm: _literals.sha_algorithm_literal = "sha1",
            multiple: bool = False,
        ) -> Project.Version | list[Project.Version]:
            """Get a version by hash.

            Args:
                hash_ (str): The hash of the file, considering its byte content, and encoded in hexadecimal
                algorithm (Literal["sha512", "sha1"]): The algorithm of the hash
                multiple (bool): Whether to return multiple results when looking for this hash

            Raises:
                NotFoundError: The requested version file wasn't found or no authorization to see this version
                InvalidRequestError: Invalid request

            Returns:
                (Project.Version): The version that was found
            """
            raw_response = _requests.get(
                f"https://api.modrinth.com/v2/version_file/{hash_}",
                params={"algorithm": algorithm, "multiple": str(multiple).lower()},
                timeout=60,
            )
            match raw_response.status_code:
                case 404:
                    raise _exceptions.NotFoundError(
                        "The requested version file wasn't found or no authorization to see this version"
                    )
            if not raw_response.ok:
                raise _exceptions.InvalidRequestError(raw_response.text)
            response: dict = raw_response.json()
            if isinstance(response, list):
                return [
                    Project.Version(_models.VersionModel._from_json(version))
                    for version in response
                ]
            return Project.Version(_models.VersionModel._from_json(response))

        @staticmethod
        def delete_file_from_hash(
            auth: str,
            hash_: str,
            version_id: str,
            algorithm: _literals.sha_algorithm_literal = "sha1",
        ) -> bool:
            """Delete a file from its hash.

            Args:
                hash_ (str): The hash of the file, considering its byte content, and encoded in hexadecimal
                algorithm (Literal["sha512", "sha1"]): The algorithm of the hash
                version_id (bool): Version ID to delete the version from if multiple files of the same hash exist
                auth (str): The authorization token to use when deleting the file from its hash

            Raises:
                NotFoundError: The requested version wasn't found
                NoAuthorizationError: No authorization to delete this file
                InvalidRequestError: Invalid request

            Returns:
                (bool): If the file deletion was successful
            """
            raw_response = _requests.delete(
                f"https://api.modrinth.com/v2/version_file/{hash_}",
                params={"algorithm": algorithm, "version_id": version_id},
                headers={"authorization": auth},
                timeout=60,
            )
            match raw_response.status_code:
                case 404:
                    raise _exceptions.NotFoundError(
                        "The requested version was not found"
                    )
                case 401:
                    raise _exceptions.NoAuthorizationError(
                        "No authorization to delete this file"
                    )
            if not raw_response.ok:
                raise _exceptions.InvalidRequestError(raw_response.text)
            return True

        @property
        def files(self) -> list[Project._File]:
            return [Project._File._from_json(file) for file in self.version_model.file_parts]  # type: ignore

        def download(self, recursive: bool = False) -> None:
            """Download the files associated with the version.

            Args:
                recursive (bool, optional): Whether to also download the files of the dependencies
            """
            for file in self.files:
                file_content = _requests.get(file.url, timeout=60).content
                open(file.name, "wb").write(file_content)
            if recursive:
                dependencies = self.dependencies
                for dep in dependencies:
                    files = dep.version.files
                    for file in files:
                        file_content = _requests.get(file.url, timeout=60).content
                        open(file.name, "wb").write(file_content)

        @property
        def project(self) -> Project:
            return Project.get(self.version_model.project_id)

        @property
        def primary_files(self) -> list[Project._File]:
            result = []
            for file in self.files:
                if file.primary:
                    result.append(file)
            return result

        @property
        def author(self) -> _users.User:
            user = _users.User.get(self.version_model.author_id)
            return user

        def is_featured(self) -> bool:
            """Check if the version is featured.

            Returns:
                (bool): Whether the version is featured
            """
            return self.version_model.featured

        @property
        def date_published(self) -> _datetime.datetime:
            return _util.format_time(self.version_model.date_published)

        @property
        def downloads(self) -> int:
            return self.version_model.downloads

        @property
        def name(self) -> str:
            return self.version_model.name

        @property
        def version_number(self) -> str:
            return self.version_model.version_number

        def __repr__(self) -> str:
            return f"Version: {self.version_model.name}"

    class GalleryImage:
        """
        Represents an image in a gallery.

        Attributes:
            file_path (str): The path to the image
            ext (str): Image extension
            featured (str): Whether an image is featured
            title (str): Title of the image
            description (str): Description of the image
            ordering (int): Ordering of the image

        """

        def __init__(
            self,
            file_path: str,
            featured: bool,
            title: str,
            description: str,
            ordering: int = 0,
        ) -> None:
            self.file_path = file_path
            self.ext = file_path.split(".")[-1]
            self.featured = str(featured).lower()
            self.title = title
            self.description = description
            self.ordering = ordering

        @staticmethod
        def _from_json(json_: dict) -> Project.GalleryImage:
            return Project.GalleryImage(
                json_.get("url", ...),
                json_.get("featured", ...),
                json_.get("title", ...),
                json_.get("description", ...),
                json_.get("ordering", ...),
            )

        def _to_json(self) -> dict:
            return _util.remove_null_values(self.__dict__)

    class _File:
        hashes: dict
        url: str
        name: str
        primary: str
        size: int
        file_type: str
        extension: str

        def is_resourcepack(self) -> bool:
            """
            Check if a file is a resourcepack.

            Returns:
                (bool): If the file is a resourcepack
            """
            if self.file_type is None:
                return False
            return True

        @staticmethod
        def _from_json(json_: dict) -> Project._File:
            result = Project._File()
            result.hashes = json_.get("hashes", ...)
            result.url = json_.get("url", ...)
            result.name = json_.get("filename", ...)
            result.primary = json_.get("primary", ...)
            result.size = json_.get("size", ...)
            result.file_type = json_.get("file_type", ...)
            result.extension = result.name.split(".")[-1]
            return result

        def __repr__(self) -> str:
            return f"File: {self.name}"

    @dataclasses.dataclass
    class License:
        """
        Represents a license.

        Attributes:
            id (str): The SPDX license ID of a project
            name (str): The long name of a license
            url (str): The URL to this license

        """

        id_: str
        name: str
        url: str | None = None

        @staticmethod
        def _from_json(license_json: dict) -> Project.License:
            result = Project.License(
                license_json["id"], license_json["name"], license_json["url"]
            )
            return result

        def _to_json(self) -> dict:
            return self.__dict__

        def __repr__(self) -> str:
            return f"License: {(self.name if self.name else self.id_)}"

    @dataclasses.dataclass
    class Donation:
        """
        Represents a donation.

        Attributes:
            id_ (str): The ID of the donation platform
            platform (str): The donation platform this link is to
            url (str): The URL of the donation platform and user

        """

        id_: str
        platform: str
        url: str

        @staticmethod
        def _from_json(donation_json: dict) -> Project.Donation:
            result = Project.Donation._from_json(donation_json)
            return result

        def __repr__(self) -> str:
            return f"Donation: {self.platform}"

    @dataclasses.dataclass
    class Dependency:
        dependency_type: _literals.dependency_type_literal
        version_id: str | None = None
        project_id: str | None = None
        file_name: str | None = None

        def _to_json(self) -> dict:
            return self.__dict__

        @staticmethod
        def _from_json(json_: dict) -> Project.Dependency:
            result = Project.Dependency(
                json_["version_id"],
                json_["project_id"],
                json_["dependency_type"],
                json_["file_name"],
            )
            return result

        @property
        def version(self) -> Project.Version:
            id = self.project_id
            if self.version_id:
                id = self.version_id
            return Project.Version.get(id)  # type: ignore

        def is_required(self) -> bool:
            """
            Check if the dependency is required.

            Returns:
                (bool): True if the dependency is required, False otherwise
            """
            return True if self.dependency_type == "required" else False

        def is_optional(self) -> bool:
            """
            Check if the dependency is optional.

            Returns:
                (bool): True if the dependency is optional, False otherwise
            """
            return True if self.dependency_type == "optional" else False

        def is_incompatible(self) -> bool:
            """
            Check if the dependency is incompatible.

            Returns:
                (bool): True if the dependency is incompatible, False otherwise
            """
            return True if self.dependency_type == "incompatible" else False

        def __repr__(self) -> str:
            return f"Dependency"

    @dataclasses.dataclass
    class _SearchResult:
        search_result_model: _models._SearchResultModel

        def __repr__(self) -> str:
            return f"Search Result: {self.search_result_model.title}"
