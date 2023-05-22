"""Projects can be mods or modpacks and are created by users"""

import datetime as dt
import json
import typing

import requests as r

import pyrinth.exceptions as exceptions
import pyrinth.literals as literals
import pyrinth.models as models
import pyrinth.modrinth as modrinth
import pyrinth.users as users
import pyrinth.util as util
import pyrinth.teams as teams


class Project:
    """Projects can be mods or modpacks and are created by users

    Attributes:
        model (ProjectModel): The project's model
    """

    def __init__(self, project_model: "models.ProjectModel") -> None:
        """
        Args:
            project_model (ProjectModel): The project's model
        """
        if isinstance(project_model, dict):
            project_model = models.ProjectModel._from_json(project_model)
        self.model = project_model

    def get_donations(self) -> list["Project.Donation"]:
        """Gets the project's donations

        Returns:
            (list[Donation]): The project's donations
        """
        return util.list_to_object(Project.Donation, self.model.donation_urls)

    def _get_auth(self, auth: str | None) -> str:
        if auth:
            return auth
        return self.model.auth  # type: ignore

    @staticmethod
    def get(id_: str, auth: object = None) -> "Project":
        """Gets a project based on an ID

        Args:
            id_ (str): The ID or slug of the project
            auth (str, optional): An optional authorization token when getting the project

        Raises:
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (Project): The project that was found
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{id_}",
            headers={"authorization": auth},  # type: ignore
            timeout=60,
        )
        match raw_response.status_code:
            case 404:
                raise exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )
        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        response.update({"authorization": auth})
        return Project(response)

    @staticmethod
    def get_multiple(ids: list[str]) -> list["Project"]:
        """Gets multiple projects

        Args:
            ids (list[str]): The IDs of the projects

        Raises:
            InvalidRequestError: Invalid request

        Returns:
            (list[Project]): The projects that were found
        """
        raw_response = r.get(
            "https://api.modrinth.com/v2/projects",
            params={"ids": json.dumps(ids)},
            timeout=60,
        )
        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return [Project(project) for project in response]

    def get_latest_version(
        self,
        loaders: list[str] | None = None,
        game_versions: list[str] | None = None,
        featured: bool | None = None,
        types: literals.version_type_literal | None = None,
        auth: str | None = None,
    ) -> "Project.Version":
        """Gets this project's latest version

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

        return versions[0]

    def get_gallery(self) -> list["Project.GalleryImage"]:
        """Gets the project's gallery

        Returns:
            (list[Project.GalleryImage]): The project's gallery images
        """
        result = util.list_to_object(Project.GalleryImage, self.model.gallery)

        return result

    def is_client_side(self) -> bool:
        """Checks if this project is client side

        Returns:
            (bool): Whether this project is client side
        """
        return True if self.model.client_side == "required" else False

    def is_server_side(self) -> bool:
        """Checks if this project is server side

        Returns:
            (bool): Whether this project is server side
        """
        return True if self.model.server_side == "required" else False

    def get_downloads(self) -> int:
        """Gets the number of downloads this project has

        Returns:
            (int): The number of downloads for this project
        """
        return self.model.downloads  # type: ignore

    def get_categories(self) -> list[str]:
        """Gets this projects categories

        Returns:
            (list[str]): The categories associated with this project
        """
        return self.model.categories

    def get_additional_categories(self) -> list[str]:
        """Gets this projects additional categories

        Returns:
            (list[str]): The additional categories associated with this project
        """
        return self.model.additional_categories  # type: ignore

    def get_all_categories(self) -> list[str]:
        """Gets this projects categories and additional categories

        Returns:
            (list[str]): The categories and additional categories associated with this project
        """
        return self.get_categories() + self.get_additional_categories()

    def get_license(self) -> "Project.License":
        """Gets this project license

        Returns:
            (Project.License): The license associated with this project
        """
        return Project.License._from_json(self.model.license)

    def get_specific_version(
        self, semantic_version: str
    ) -> typing.Optional["Project.Version"]:
        """Gets a specific version based on the semantic version

        Args:
            semantic_version (str): The semantic version to search for

        Returns:
            (Project.Version): The version that was found using the semantic version
            (None): No version was found with that semantic version
        """
        versions = self.get_versions()
        if versions:
            for version in versions:
                if version.model.version_number == semantic_version:
                    return version

        return None

    def download(self, recursive: bool = False) -> None:
        """Downloads this project

        Args:
            recursive (bool): Whether to download dependencies. Defaults to False
        """
        latest = self.get_latest_version()
        files = latest.get_files()
        for file in files:
            file_content = r.get(file.url).content
            open(file.name, "wb").write(file_content)

        if recursive:
            dependencies = latest.get_dependencies()
            for dep in dependencies:
                files = dep.get_version().get_files()
                for file in files:
                    file_content = r.get(file.url).content
                    open(file.name, "wb").write(file_content)

    def get_versions(
        self,
        loaders: list[str] | None = None,
        game_versions: list[str] | None = None,
        featured: bool | None = None,
        types: literals.version_type_literal | None = None,
        auth: str | None = None,
    ) -> list["Project.Version"]:
        """Gets project versions based on filters

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

        filters = util.remove_null_values(filters)
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/version",
            params=util.json_to_query_params(filters),
            headers={"authorization": self._get_auth(auth)},
            timeout=60,
        )

        match raw_response.status_code:
            case 404:
                raise exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = raw_response.json()

        versions = [
            self.Version(models.VersionModel._from_json(version))
            for version in response
        ]

        if not types:
            return versions

        result = []
        for version in versions:
            if version.model.version_type in types:
                result.append(version)

        return result

    def get_oldest_version(
        self,
        loaders: list[str] | None = None,
        game_versions: list[str] | None = None,
        featured: bool | None = None,
        types: literals.version_type_literal | None = None,
        auth: str | None = None,
    ) -> "Project.Version":
        """Gets the oldest project version

        Args:
            loaders (list[str], optional): The types of loaders to filter for
            game_versions (list[str], optional): The game versions to filter for
            featured (bool, optional): Allows to filter for featured or non-featured versions only
            types (Literal["release", "beta", "alpha"], optional): The type of version
            auth (str, optional): An optional authorization token to use when getting the project versions

        Returns:
            (Project.Version): The version that was found
        """
        versions = self.get_versions(loaders, game_versions, featured, types, auth)

        return versions[-1]

    def get_id(self) -> str:
        """Gets the ID of the project

        Returns:
            (str): The ID of the project
        """
        return self.model.id  # type: ignore

    def get_slug(self) -> str:
        """Gets the slug of the project

        Returns:
            (str): The slug of the project
        """
        return self.model.slug

    def get_name(self) -> str:
        """Gets the name of the project

        Returns:
            (str): The name of the project
        """
        return self.model.title

    @staticmethod
    def get_version(id_: str) -> "Project.Version":
        """Gets a version by ID

        Args:
            id_ (str): The ID of the version

        Raises:
            NotFoundError: The requested version wasn't found or no authorization to see this version
            InvalidRequestError: Invalid request

        Returns:
            (Project.Version): The version that was found
        """
        raw_response = r.get(f"https://api.modrinth.com/v2/version/{id_}", timeout=60)

        match raw_response.status_code:
            case 404:
                raise exceptions.NotFoundError(
                    "The requested version wasn't found or no authorization to see this version"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = raw_response.json()
        return Project.Version(models.VersionModel._from_json(response))

    def create_version(self, version_model, auth: str | None = None) -> int:
        """Creates a new version on the project

        Args:
            auth (str, optional): The authorization token to use when creating the version
            version_model (VersionModel): The model to use when creating the version

        Raises:
            NoAuthorizationError: No authorization to create this version
            InvalidRequestError: Invalid request

        Returns:
            (int): Whether creating the version was successful
        """
        version_model.project_id = self.model.id

        files = {"data": version_model.to_bytes()}

        for file in version_model.files:
            files.update({util.remove_file_path(file): open(file, "rb").read()})

        raw_response = r.post(
            "https://api.modrinth.com/v2/version",
            headers={"authorization": self._get_auth(auth)},
            files=files,
            timeout=60,
        )

        match raw_response.status_code:
            case 401:
                raise exceptions.NoAuthorizationError(
                    "No authorization to create this version"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def change_icon(self, file_path: str, auth: str | None = None) -> bool:
        """Changes the project icon

        Args:
            file_path (str): The file path of the image to use for the new project icon
            auth (str, optional): The authorization token to use when changing the project icon

        Raises:
            InvalidParamError: Invalid input for new icon
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the project icon change was successful
        """
        raw_response = r.patch(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/icon",
            params={"ext": file_path.split(".")[-1]},
            headers={"authorization": self._get_auth(auth)},
            data=open(file_path, "rb"),
            timeout=60,
        )

        match raw_response.status_code:
            case 400:
                raise exceptions.InvalidParamError("Invalid input for new icon")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def delete_icon(self, auth: str | None = None) -> bool:
        """Deletes the project icon

        Args:
            auth (str, optional): The authorization token to use when deleting the project icon

        Raises:
            InvalidParamError: Invalid input
            NoAuthorizationError: No authorization to edit this project
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the project icon deletion was successful
        """
        raw_response = r.delete(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/icon",
            headers={"authorization": self._get_auth(auth)},
            timeout=60,
        )

        match raw_response.status_code:
            case 400:
                raise exceptions.InvalidParamError("Invalid input")

            case 401:
                raise exceptions.NoAuthorizationError(
                    "No authorization to edit this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def add_gallery_image(
        self, image: "Project.GalleryImage", auth: str | None = None
    ) -> bool:
        """Adds a gallery image to the project

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
        raw_response = r.post(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/gallery",
            headers={"authorization": self._get_auth(auth)},
            params=image._to_json(),
            data=open(image.file_path, "rb"),
            timeout=60,
        )

        match raw_response.status_code:
            case 401:
                raise exceptions.NoAuthorizationError(
                    "No authorization to create a gallery image"
                )

            case 404:
                raise exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

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
        """Modifies a gallery image

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

        modified_json = util.remove_null_values(modified_json)

        raw_response = r.patch(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/gallery",
            params=modified_json,
            headers={"authorization": self._get_auth(auth)},
            timeout=60,
        )

        match raw_response.status_code:
            case 401:
                raise exceptions.NoAuthorizationError(
                    "No authorization to edit this gallery image"
                )

            case 404:
                raise exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def delete_gallery_image(self, url: str, auth: str | None = None) -> bool:
        """Deletes a gallery image

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
            raise exceptions.InvalidParamError(
                "Please use cdn.modrinth.com instead of cdn-raw.modrinth.com"
            )

        raw_response = r.delete(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/gallery",
            headers={"authorization": self._get_auth(auth)},
            params={"url": url},
            timeout=60,
        )

        match raw_response.status_code:
            case 400:
                raise exceptions.InvalidParamError("Invalid URL or project specified")

            case 401:
                raise exceptions.NoAuthorizationError(
                    "No authorization to delete this gallery image"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

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
        status: literals.project_status_literal | None = None,
        requested_status: literals.requested_project_status_literal | None = None,
        moderation_message: str | None = None,
        moderation_message_body: str | None = None,
        auth: str | None = None,
    ) -> bool:
        """Modifies the project

        Args:
            slug (str, optional): The slug of a project, used for vanity URLs. Regex: ^[\\w!@$()`.+,"\\-']{3,64}$
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

        modified_json = util.remove_null_values(modified_json)

        if not modified_json:
            raise exceptions.InvalidParamError(
                "Please specify at least 1 optional argument"
            )

        raw_response = r.patch(
            f"https://api.modrinth.com/v2/project/{self.model.slug}",
            data=json.dumps(modified_json),
            headers={
                "Content-Type": "application/json",
                "authorization": self._get_auth(auth),
            },
            timeout=60,
        )

        match raw_response.status_code:
            case 401:
                raise exceptions.NoAuthorizationError(
                    "No authorization to edit this project"
                )

            case 404:
                raise exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def delete(self, auth: str | None = None) -> typing.Literal[True]:
        """Deletes the project

        Args:
            auth (str, optional): Authentication token to use when deleting the project

        Raises:
            NotFoundError: The requested project wasn't found
            NoAuthorizationError: No authorization to delete this project
            InvalidRequestError: Invalid request

        Returns:
            (bool): Whether the project deletion was successful
        """
        raw_response = r.delete(
            f"https://api.modrinth.com/v2/project/{self.model.slug}",
            headers={"authorization": self._get_auth(auth)},
            timeout=60,
        )

        match raw_response.status_code:
            case 400:
                raise exceptions.NotFoundError("The requested project was not found")

            case 401:
                raise exceptions.NoAuthorizationError(
                    "No authorization to delete this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def get_dependencies(self) -> list["Project"]:
        """Gets the dependencies of the project

        Raises:
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (list[Project]): The dependencies of the project
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/dependencies",
            timeout=60,
        )

        match raw_response.status_code:
            case 404:
                raise exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = raw_response.json()
        return [Project(dependency) for dependency in response.get("projects")]

    @staticmethod
    def search(
        query: str = "",
        facets: list[list[str]] | None = None,
        index: literals.index_literal = "relevance",
        offset: int = 0,
        limit: int = 10,
        filters: list[str] | None = None,
    ) -> list["Project.SearchResult"]:
        """Searches for projects

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
            params.update({"facets": json.dumps(facets)})
        if index != "relevance":
            params.update({"index": index})
        if offset != 0:
            params.update({"offset": str(offset)})
        if limit != 10:
            params.update({"limit": str(limit)})
        if filters:
            params.update({"filters": json.dumps(filters)})
        raw_response = r.get(
            "https://api.modrinth.com/v2/search", params=params, timeout=60
        )
        response = raw_response.json()
        return [
            Project.SearchResult(models.SearchResultModel._from_json(project))
            for project in response.get("hits")
        ]

    def get_team_members(self) -> "list[teams.Team.TeamMember]":
        """Gets the team members of the project

        Returns:
            (list[Project.TeamMember)]: The team members of the project
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{self.model.id}/members", timeout=60
        )

        match raw_response.status_code:
            case 404:
                raise exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = raw_response.json()

        return [
            teams.Team.TeamMember._from_json(team_member) for team_member in response
        ]

    def get_team(self) -> "teams.Team":
        """Gets the project's team

        Raises:
            NotFoundError: The requested project wasn't found or no authorization to see this project
            InvalidRequestError: Invalid request

        Returns:
            (Team): The project's team
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{self.model.id}/members", timeout=60
        )

        match raw_response.status_code:
            case 404:
                raise exceptions.NotFoundError(
                    "The requested project wasn't found or no authorization to see this project"
                )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = raw_response.json()

        return teams.Team._from_json(response)

    def __repr__(self) -> str:
        """Returns a string representation of the Project instance

        Returns:
            (str): A string representation of the Project instance
        """
        return f"Project: {self.model.title}"

    class Version:
        """Versions contain download links to files with additional metadata

        Attributes:
            model (VersionModel): The version model associated with the version

        """

        def __init__(self, version_model: "models.VersionModel") -> None:
            """
            Args:
                version_model (VersionModel): The version model to associate with the Version object
            """
            self.model = version_model

        def get_type(self) -> str:
            """Gets the type of the version

            Returns:
                (str): The type of the version
            """
            return self.model.version_type

        def get_dependencies(self) -> list["Project.Dependency"]:
            """Gets the dependencies of the version

            Returns:
                (list[Project.Dependency]): The dependencies of the version
            """
            result = []
            for dependency in self.model.dependencies:
                result.append(Project.Dependency._from_json(dependency))
            return result

        @staticmethod
        def get(id_: str) -> "Project.Version":
            """Gets a version by ID

            Args:
                id_ (str): The ID of the version

            Raises:
                NotFoundError: The requested version wasn't found or no authorization to see this version
                InvalidRequestError: Invalid request

            Returns:
                (Project.Version): The version that was found
            """
            raw_response = r.get(
                f"https://api.modrinth.com/v2/version/{id_}", timeout=60
            )
            match raw_response.status_code:
                case 404:
                    raise exceptions.NotFoundError(
                        "The requested version wasn't found or no authorization to see this version"
                    )
            if not raw_response.ok:
                raise exceptions.InvalidRequestError(raw_response.text)
            response = raw_response.json()
            return Project.Version(models.VersionModel._from_json(response))

        @staticmethod
        def get_from_hash(
            hash_: str,
            algorithm: literals.sha_algorithm_literal = "sha1",
            multiple: bool = False,
        ) -> typing.Union["Project.Version", list["Project.Version"]]:
            """Gets a version by hash

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
            raw_response = r.get(
                f"https://api.modrinth.com/v2/version_file/{hash_}",
                params={"algorithm": algorithm, "multiple": str(multiple).lower()},
                timeout=60,
            )
            match raw_response.status_code:
                case 404:
                    raise exceptions.NotFoundError(
                        "The requested version file wasn't found or no authorization to see this version"
                    )
            if not raw_response.ok:
                raise exceptions.InvalidRequestError(raw_response.text)
            response = raw_response.json()
            if isinstance(response, list):
                return [
                    Project.Version(models.VersionModel._from_json(version))
                    for version in response
                ]
            return Project.Version(models.VersionModel._from_json(response))

        @staticmethod
        def delete_file_from_hash(
            auth: str,
            hash_: str,
            version_id: str,
            algorithm: literals.sha_algorithm_literal = "sha1",
        ) -> typing.Literal[True]:
            """Deletes a file from its hash

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
            raw_response = r.delete(
                f"https://api.modrinth.com/v2/version_file/{hash_}",
                params={"algorithm": algorithm, "version_id": version_id},
                headers={"authorization": auth},
                timeout=60,
            )
            match raw_response.status_code:
                case 404:
                    raise exceptions.NotFoundError(
                        "The requested version was not found"
                    )
                case 401:
                    raise exceptions.NoAuthorizationError(
                        "No authorization to delete this file"
                    )
            if not raw_response.ok:
                raise exceptions.InvalidRequestError(raw_response.text)
            return True

        def get_files(self) -> list["Project.File"]:
            """Gets the files associated with the version

            Returns:
                (list[Project.File]): The files associated with the version
            """
            result = []
            for file in self.model.files:
                result.append(Project.File._from_json(file))  # type: ignore
            return result

        def download(self, recursive: bool = False) -> None:
            """Downloads the files associated with the version

            Args:
                recursive (bool, optional): Whether to also download the files of the dependencies
            """
            files = self.get_files()
            for file in files:
                file_content = r.get(file.url).content
                open(file.name, "wb").write(file_content)

            if recursive:
                dependencies = self.get_dependencies()
                for dep in dependencies:
                    files = dep.get_version().get_files()
                    for file in files:
                        file_content = r.get(file.url).content
                        open(file.name, "wb").write(file_content)

        def get_project(self) -> "Project":
            """Gets the project associated with the version

            Returns:
                (Project): The project associated with the version
            """
            return modrinth.Modrinth.get_project(self.model.project_id)  # type: ignore

        def get_primary_files(self) -> list["Project.File"]:
            """Gets the primary files associated with the version

            Returns:
                (list[Project.File]): The primary files associated with the version
            """
            result = []
            for file in self.get_files():
                if file.primary:
                    result.append(file)
            return result

        def get_author(self) -> "users.User":
            """Gets the author of the version

            Returns:
                (User): The author of the version
            """
            user = users.User.get(self.model.author_id)  # type: ignore
            return user

        def is_featured(self) -> bool:
            """Checks if the version is featured

            Returns:
                (bool): Whether the version is featured
            """
            return self.model.featured

        def get_date_published(self) -> "dt.datetime":
            """Gets the date when the version was published

            Returns:
                (datetime): The date when the version was published
            """
            return util.format_time(self.model.date_published)

        def get_downloads(self) -> int:
            """Gets the number of downloads for the version

            Returns:
                (int): The number of downloads of the version
            """
            return self.model.downloads  # type: ignore

        def get_name(self) -> str:
            """Gets the name of the version

            Returns:
                (str): The name of the version
            """
            return self.model.name

        def get_version_number(self) -> str:
            """Gets the version number of the version

            Returns:
                (str): The version number of the version
            """
            return self.model.version_number

        def __repr__(self) -> str:
            return f"Version: {self.model.name}"

    class GalleryImage:
        """
        Represents an image in a gallery

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
            """
            Initializes a GalleryImage object

            Args:
                file_path (str): The path to the image
                featured (str): Whether an image is featured
                title (str): Title of the image
                description (str): Description of the image
                ordering (int): Ordering of the image
            """
            self.file_path = file_path
            self.ext = file_path.split(".")[-1]
            self.featured = str(featured).lower()
            self.title = title
            self.description = description
            self.ordering = ordering

        @staticmethod
        def _from_json(json_: dict) -> "Project.GalleryImage":
            return Project.GalleryImage(
                json_.get("url"),  # type: ignore
                json_.get("featured"),  # type: ignore
                json_.get("title"),  # type: ignore
                json_.get("description"),  # type: ignore
                json_.get("ordering"),  # type: ignore
            )

        def _to_json(self) -> dict:
            return util.remove_null_values(self.__dict__)

    class File:
        """
        Represents a file with various attributes and methods

        Attributes:
            hashes (dict[str, str]): A dictionary of hash algorithms and their corresponding hash values for the file
            url (str): The URL where the file can be downloaded
            name (str): The name of the file
            primary (str): The primary hash algorithm used to verify the file's integrity
            size (int): The size of the file in bytes
            file_type (str): The type of the file
            extension (str): The file extension

        """

        def __init__(
            self,
            hashes: dict[str, str],
            url: str,
            filename: str,
            primary: str,
            size: int,
            file_type: str,
        ) -> None:
            """
            Initializes a File object

            Args:
                hashes (dict[str, str]): A dictionary of hash algorithms and their corresponding hash values for the file
                url (str): The URL where the file can be downloaded
                filename (str): The name of the file
                primary (str): The primary hash algorithm used to verify the file's integrity
                size (int): The size of the file in bytes
                file_type (str): The type of the file
            """
            self.hashes = hashes
            self.url = url
            self.name = filename
            self.primary = primary
            self.size = size
            self.file_type = file_type
            self.extension = filename.split(".")[-1]

        def is_resourcepack(self) -> bool:
            """
            Checks if a file is a resourcepack

            Returns:
                (bool): If the file is a resourcepack
            """
            if self.file_type is None:
                return False
            return True

        @staticmethod
        def _from_json(json_: dict) -> "Project.File":
            result = Project.File(
                json_.get("hashes"),  # type: ignore
                json_.get("url"),  # type: ignore
                json_.get("filename"),  # type: ignore
                json_.get("primary"),  # type: ignore
                json_.get("size"),  # type: ignore
                json_.get("file_type"),  # type: ignore
            )
            return result

        def __repr__(self) -> str:
            return f"File: {self.name}"

    class License:
        """
        Represents a license

        Attributes:
            id (str): The SPDX license ID of a project
            name (str): The long name of a license
            url (str): The URL to this license

        """

        def __init__(self, id_: str, name: str, url: str | None = None) -> None:
            """
            Initializes a License object

            Args:
                id_ (str): The SPDX license ID of a project
                name (str): The long name of a license
                url (str): The URL to this license
            """
            self.id = id_
            self.name = name
            self.url = url

        @staticmethod
        def _from_json(json_: dict) -> "Project.License":
            result = Project.License(
                json_.get("id"),  # type: ignore
                json_.get("name"),  # type: ignore
                json_.get("url"),  # type: ignore
            )

            return result

        def _to_json(self) -> dict:
            return self.__dict__

        def __repr__(self) -> str:
            return f"License: {self.name if self.name else self.id}"

    class Donation:
        """
        Represents a donation

        Attributes:
            id (str): The ID of the donation platform
            platform (str): The donation platform this link is to
            url (str): The URL of the donation platform and user

        """

        def __init__(self, id_: str, platform: str, url: str) -> None:
            """
            Initializes a Donation object

            Args:
                id_ (str): The ID of the donation
                platform (str): The platform used for the donation
                url (str): The URL to the donation page
            """
            self.id = id_
            self.platform = platform
            self.url = url

        @staticmethod
        def _from_json(json_: dict) -> "Project.Donation":
            result = Project.Donation(
                json_.get("id"),  # type: ignore
                json_.get("platform"),  # type: ignore
                json_.get("url"),  # type: ignore
            )

            return result

        def __repr__(self) -> str:
            return f"Donation: {self.platform}"

    class Dependency:
        """
        Represents a dependency

        Attributes:
            file_name (str): The name of the dependency
            version_id (str): The ID of the dependency's version
            project_id (str): The ID of the dependency's project
            dependency_option (str): The option for the dependency
        """

        def __init__(self) -> None:
            self.dependency_option: str | None = None
            self.file_name: str | None = None
            self.version_id: str | None = None
            self.project_id: str | None = None

        def _to_json(self) -> dict:
            return self.__dict__

        @staticmethod
        def _from_json(json_: dict) -> "Project.Dependency":
            result = Project.Dependency()
            result.version_id = json_.get("version_id")
            result.project_id = json_.get("project_id")
            result.dependency_option = json_.get("dependency_option")
            result.file_name = json_.get("file_name")
            return result

        def get_version(self) -> "Project.Version":
            id_ = self.project_id
            if self.version_id:
                id_ = self.version_id
            return Project.Version.get(id_)  # type: ignore

        def is_required(self) -> bool:
            """
            Checks if the dependency is required

            Returns:
                (bool): True if the dependency is required, False otherwise
            """
            return True if self.dependency_option == "required" else False

        def is_optional(self) -> bool:
            """
            Checks if the dependency is optional

            Returns:
                (bool): True if the dependency is optional, False otherwise
            """
            return True if self.dependency_option == "optional" else False

        def is_incompatible(self) -> bool:
            """
            Checks if the dependency is incompatible

            Returns:
                (bool): True if the dependency is incompatible, False otherwise
            """
            return True if self.dependency_option == "incompatible" else False

    class SearchResult:
        """
        Represents a search result

        Attributes:
            model (SearchResultModel): The search result model

        """

        def __init__(self, search_result_model: "models.SearchResultModel") -> None:
            """
            Initializes a SearchResult object

            Args:
                search_result_model (SearchResultModel): The search result model or a dictionary representing the search result model
            """
            self.model = search_result_model

        def __repr__(self) -> str:
            return f"Search Result: {self.model.title}"
