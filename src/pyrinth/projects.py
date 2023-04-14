"""User projects."""

import datetime
import json
import typing

import requests as r

import pyrinth.exceptions as exceptions
import pyrinth.literals as literals
import pyrinth.models as models
import pyrinth.modrinth as modrinth
import pyrinth.users as users
import pyrinth.util as util


class Project:
    """Contains information about a users projects."""

    def __init__(self, project_model) -> None:
        if isinstance(project_model, dict):
            project_model = models.ProjectModel.from_json(project_model)
        self.model = project_model

    def __repr__(self) -> str:
        return f"Project: {self.model.title}"

    def get_donations(self) -> list["Project.Donation"]:
        """Gets this project's donations.

        Returns:
            list[Donation]: The donations that this project has.
        """
        return util.list_to_object(Project.Donation, self.model.donation_urls)

    def get_auth(self, auth: typing.Optional[str]) -> str:
        """Utility Function."""
        if auth:
            return auth
        return self.model.auth  # type: ignore

    @staticmethod
    def get(id_: str, auth: object = None) -> "Project":
        """Gets a project based on an ID.

        Args:
            id_ (str): The project's ID to get.
            auth (str, optional): An optional authorization token when getting the project. Defaults to None.

        Raises:
            NotFoundError: The project wasn't found.
            InvalidRequestError: An invalid API call was sent.

        Returns:
            Project: The project that was found.
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{id_}",
            headers={"authorization": auth},  # type: ignore
            timeout=60,
        )
        if raw_response.status_code == 404:
            raise exceptions.NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )
        if not raw_response.ok:
            raise exceptions.InvalidRequestError()
        response = json.loads(raw_response.content)
        response.update({"authorization": auth})
        return Project(response)

    @staticmethod
    def get_multiple(ids: list[str]) -> list["Project"]:
        """Gets multiple projects.

        Raises:
            InvalidRequestError: An invalid API call was sent.

        Returns:
            list[Project]: The projects that were found.
        """
        raw_response = r.get(
            "https://api.modrinth.com/v2/projects",
            params={"ids": json.dumps(ids)},
            timeout=60,
        )
        if not raw_response.ok:
            raise exceptions.InvalidRequestError()
        response = json.loads(raw_response.content)
        return [Project(project) for project in response]

    def get_latest_version(
        self,
        loaders: typing.Optional[list[str]] = None,
        game_versions: typing.Optional[list[str]] = None,
        featured: typing.Optional[bool] = None,
        types: typing.Optional[literals.version_type_literal] = None,
        auth: typing.Optional[str] = None,
    ) -> "Project.Version":
        """Gets this project's latest version.

        Args:
            loaders (list[str]): The loaders filter. Defaults to None.
            game_versions (list[str]): The game versions filter. Defaults to None.
            featured (bool): The is featured filter. Defaults to None.
            types (list[str]): The types filter. Defaults to None.
            auth (str): The authorization token. Defaults to None.

        Returns:
            Version: The project's latest version.
        """
        versions = self.get_versions(
            loaders, game_versions, featured, types, auth)

        return versions[0]

    def get_gallery(self) -> list["Project.GalleryImage"]:
        """Gets the project's gallery

        Returns:
            list[GalleryImage]: The project's gallery images
        """
        result = util.list_to_object(Project.GalleryImage, self.model.gallery)

        return result

    def is_client_side(self) -> bool:
        """Checks if this project is client side."""
        return True if self.model.client_side == "required" else False

    def is_server_side(self) -> bool:
        """Checks if this project is server side."""
        return True if self.model.server_side == "required" else False

    def get_downloads(self) -> int:
        """Gets the amount of downloads this project has."""
        return self.model.downloads  # type: ignore

    def get_categories(self) -> list[str]:
        """Gets this projects categories."""
        return self.model.categories

    def get_additional_categories(self) -> list[str]:
        """Gets this projects additional categories."""
        return self.model.additional_categories  # type: ignore

    def get_all_categories(self) -> list[str]:
        """Gets this projects categories and additional categories."""
        return self.get_categories() + self.get_additional_categories()

    def get_license(self) -> "Project.License":
        """Gets this projects license."""
        return Project.License.from_json(self.model.license)

    def get_specific_version(
        self, semantic_version: str
    ) -> typing.Optional["Project.Version"]:
        """
        Gets a specific project version based on the semantic version.

        Returns:
            Project.Version: The version that was found using the semantic version
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
            recursive (bool): Download dependencies
        """
        latest = self.get_latest_version()
        files = latest.get_files()
        for file in files:
            file_content = r.get(file.url).content
            open(file.filename, "wb").write(file_content)

        if recursive:
            dependencies = latest.get_dependencies()
            for dep in dependencies:
                files = dep.get_version().get_files()
                for file in files:
                    file_content = r.get(file.url).content
                    open(file.filename, "wb").write(file_content)

    def get_versions(
        self,
        loaders: typing.Optional[list[str]] = None,
        game_versions: typing.Optional[list[str]] = None,
        featured: typing.Optional[bool] = None,
        types: typing.Optional[literals.version_type_literal] = None,
        auth=None,
    ) -> list["Project.Version"]:
        """
        Gets project versions based on filters.

        Returns:
            list[Project.Version]: The versions that were found using the filters
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
            headers={"authorization": self.get_auth(auth)},
            timeout=60,
        )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        response = json.loads(raw_response.content)

        versions = [self.Version(version) for version in response]

        if not types:
            return versions

        result = []
        for version in versions:
            if version.model.version_type in types:
                result.append(version)

        return result

    def get_oldest_version(
        self,
        loaders: typing.Optional[list[str]] = None,
        game_versions: typing.Optional[list[str]] = None,
        featured: typing.Optional[bool] = None,
        types: typing.Optional[literals.version_type_literal] = None,
        auth=None,
    ) -> "Project.Version":
        """
        Gets the oldest project version.

        Returns:
            Project.Version: The oldest project version
        """
        versions = self.get_versions(
            loaders, game_versions, featured, types, auth)

        return versions[-1]

    def get_id(self) -> str:
        """
        Gets the ID of the project.

        Returns:
            str: The ID of the project
        """
        return self.model.id  # type: ignore

    def get_slug(self) -> str:
        """
        Gets the slug of the project.

        Returns:
            str: The slug of the project
        """
        return self.model.slug

    def get_name(self) -> str:
        """
        Gets the name of the project.

        Returns:
            str: The name of the project
        """
        return self.model.title

    @staticmethod
    def get_version(id_: str) -> "Project.Version":
        """
        Gets a version by ID.

        Returns:
            Project.Version: The version that was found using the ID
            None: The version was not found
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/version/{id_}", timeout=60)

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        response = json.loads(raw_response.content)
        return Project.Version(response)

    def create_version(self, version_model, auth=None) -> int:
        """
        Creates a new version on the project.

        Args:
            auth (str): The authorization token to use when creating a version
            version_model (VersionModel): The VersionModel to use for the new project version

        Returns:
            int: If creating the new project version was successful
        """
        version_model.project_id = self.model.id

        files = {"data": version_model.to_bytes()}

        for file in version_model.files:
            files.update({util.remove_file_path(
                file): open(file, "rb").read()})

        raw_response = r.post(
            "https://api.modrinth.com/v2/version",
            headers={"authorization": self.get_auth(auth)},
            files=files,
            timeout=60,
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to create this version"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        return True

    def change_icon(self, file_path: str, auth=None) -> int:
        """
        Changes the projects icon.

        Args:
            file_path (str): The file path of the image to use for the new project icon
            auth (str): The authorization token to use when changing the projects icon

        Returns:
            int: If the project icon change was successful
        """
        raw_response = r.patch(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/icon",
            params={"ext": file_path.split(".")[-1]},
            headers={"authorization": self.get_auth(auth)},
            data=open(file_path, "rb"),
            timeout=60,
        )

        if raw_response.status_code == 400:
            raise exceptions.InvalidParamError("Invalid input for new icon")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        return True

    def delete_icon(self, auth=None) -> int:
        """
        Deletes the projects icon.

        Args:
            auth (str): The authorization token to use when deleting the projects icon

        Returns:
            int: If the project icon deletion was successful
        """
        raw_response = r.delete(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/icon",
            headers={"authorization": self.get_auth(auth)},
            timeout=60,
        )

        if raw_response.status_code == 400:
            raise exceptions.InvalidParamError("Invalid input")

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to edit this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        return True

    def add_gallery_image(self, image: "Project.GalleryImage", auth=None) -> int:
        """
        Adds a gallery image to the project.

        Args:
            auth (str): The authorization token to use when adding the gallery image.
            image (Project.GalleryImage): The gallery image to add.

        Returns:
            int: If the gallery image addition was successful
        """
        raw_response = r.post(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/gallery",
            headers={"authorization": self.get_auth(auth)},
            params=image.to_json(),
            data=open(image.file_path, "rb"),
            timeout=60,
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to create a gallery image"
            )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        return True

    def modify_gallery_image(
        self,
        url: str,
        featured: typing.Optional[bool] = None,
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        ordering: typing.Optional[int] = None,
        auth=None,
    ) -> int:
        """
        Modifies a project gallery image.

        Args:
            auth (str): The authorization token to use when modifying the gallery image
            url (str): The url of the gallery image
            featured (typing.Optional[bool]): If the new gallery image is featured. Defaults to None.
            title (typing.Optional[str]): The new gallery image title. Defaults to None.
            description (typing.Optional[str]): The new gallery image description. Defaults to None.
            ordering (typing.Optional[int]): The new gallery image ordering. Defaults to None.

        Returns:
            int: If the gallery image modification was successful
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
            headers={"authorization": self.get_auth(auth)},
            timeout=60,
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to edit this gallery image"
            )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        return True

    def delete_gallery_image(self, url: str, auth=None) -> int:
        """
        Deletes a projects gallery image.

        Args:
            url (str): The url of the gallery image
            auth (str): The authorization token to use when deleting the gallery image

        Raises:
            Exception: If the user used cdn-raw.modrinth.com instead of cdn.modrinth.com

        Returns:
            int: If the gallery image deletion was successful
        """
        if "-raw" in url:
            raise exceptions.InvalidParamError(
                "Please use cdn.modrinth.com instead of cdn-raw.modrinth.com"
            )

        raw_response = r.delete(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/gallery",
            headers={"authorization": self.get_auth(auth)},
            params={"url": url},
            timeout=60,
        )

        if raw_response.status_code == 400:
            raise exceptions.InvalidParamError(
                "Invalid URL or project specified")

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to delete this gallery image"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        return True

    def modify(
        self,
        slug: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        categories: typing.Optional[list[str]] = None,
        client_side: typing.Optional[str] = None,
        server_side: typing.Optional[str] = None,
        body: typing.Optional[str] = None,
        additional_categories: typing.Optional[list[str]] = None,
        issues_url: typing.Optional[str] = None,
        source_url: typing.Optional[str] = None,
        wiki_url: typing.Optional[str] = None,
        discord_url: typing.Optional[str] = None,
        license_id: typing.Optional[str] = None,
        license_url: typing.Optional[str] = None,
        status: typing.Optional[literals.project_status_literal] = None,
        requested_status: typing.Optional[
            literals.requested_project_status_literal
        ] = None,
        moderation_message: typing.Optional[str] = None,
        moderation_message_body: typing.Optional[str] = None,
        auth=None,
    ) -> int:
        """
        Modifies a project.

        Args:
            auth (str): The authorization token to use to modify the project
            slug (typing.Optional[str]): The new project slug. Defaults to None.
            title (typing.Optional[str]): The new project title. Defaults to None.
            description (typing.Optional[str]): The new project description. Defaults to None.
            categories (typing.Optional[list[str]]): The new project categories. Defaults to None.
            client_side (typing.Optional[str]): If the project is supported on client_side. Defaults to None.
            server_side (typing.Optional[str]): If the project is supported on the server side. Defaults to None.
            body (typing.Optional[str]): The new project body. Defaults to None.
            additional_categories (typing.Optional[list[str]]): The new project additional categories. Defaults to None.
            issues_url (typing.Optional[str]): The new project issues url. Defaults to None.
            source_url (typing.Optional[str]): The new project source url. Defaults to None.
            wiki_url (typing.Optional[str]): The new project wiki url. Defaults to None.
            discord_url (typing.Optional[str]): The new project discord url. Defaults to None.
            license_id (typing.Optional[str]): The new project license id. Defaults to None.
            license_url (typing.Optional[str]): The new project license url. Defaults to None.
            status (typing.Optional[str]): The new project status. Defaults to None.
            requested_status (typing.Optional[str]): The new project requested status. Defaults to None.
            moderation_message (typing.Optional[str]): The new project moderation message. Defaults to None.
            moderation_message_body (typing.Optional[str]): The new project moderation message body. Defaults to None.

        Raises:
            Exception: If no new project arguments are specified

        Returns:
            int: If the project modification was successful
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
                "Please specify at least 1 optional argument."
            )

        raw_response = r.patch(
            f"https://api.modrinth.com/v2/project/{self.model.slug}",
            data=json.dumps(modified_json),
            headers={
                "Content-Type": "application/json",
                "authorization": self.get_auth(auth),
            },
            timeout=60,
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to edit this project"
            )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        return True

    def delete(self, auth=None) -> int:
        """
        Deletes the project.

        Args:
            auth (str): The authorization token to delete the project

        Returns:
            int: If the deletion was successful
        """
        raw_response = r.delete(
            f"https://api.modrinth.com/v2/project/{self.model.slug}",
            headers={"authorization": self.get_auth(auth)},
            timeout=60,
        )

        if raw_response.status_code == 400:
            raise exceptions.NotFoundError(
                "The requested project was not found")

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to delete this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        return True

    def get_dependencies(self) -> list["Project"]:
        """
        Gets a projects dependencies.

        Returns:
            list[Project]: The projects dependencies
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{self.model.slug}/dependencies",
            timeout=60,
        )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        response = json.loads(raw_response.content)
        return [Project(dependency) for dependency in response.get("projects")]

    @staticmethod
    def search(
        query: str = "",
        facets: typing.Optional[list[list[str]]] = None,
        index: literals.index_literal = "relevance",
        offset: int = 0,
        limit: int = 10,
        filters: typing.Optional[list[str]] = None,
    ) -> list["SearchResult"]:
        """Searches projects on modrinth

        Raises:
            InvalidRequestError: An invalid API call was sent.

        Returns:
            list[SearchResult]: The results that were found.
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
        if not raw_response.ok:
            raise exceptions.InvalidRequestError()
        response = json.loads(raw_response.content)
        return [Project.SearchResult(project) for project in response.get("hits")]

    def get_team_members(self) -> "list[Project.TeamMember]":
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{self.model.id}/members", timeout=60
        )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        response = json.loads(raw_response.content)

        return [Project.TeamMember.from_json(team_member) for team_member in response]

    class TeamMember:
        def __init__(
            self, team_id, user, role, permissions, accepted, payouts_split, ordering
        ) -> None:
            self.team_id = team_id
            self.user = user
            self.role = role
            self.permissions = permissions
            self.accepted = accepted
            self.payouts_split = payouts_split
            self.ordering = ordering

        def __repr__(self) -> str:
            return f"Team Member"

        def get_user(self) -> "users.User":
            return users.User.from_json(self.user)

        @staticmethod
        def from_json(json):
            result = Project.TeamMember(
                json.get("user"),
                json.get("user"),
                json.get("role"),
                json.get("permissions"),
                json.get("accepted"),
                json.get("payouts_split"),
                json.get("ordering"),
            )
            return result

    class Version:
        """Used for a projects versions."""

        def __init__(self, version_model) -> None:
            if isinstance(version_model, dict):
                version_model = models.VersionModel.from_json(version_model)
                self.model = version_model
            self.model = version_model

        def get_type(self) -> str:
            """Gets the versions type (release / beta / alpha)."""
            return self.model.version_type

        def get_dependencies(self) -> list["Project.Dependency"]:
            """
            Gets a projects dependencies.

            Returns:
                list[Project.Dependency]: The projects dependencies
            """
            result = []
            for dependency in self.model.dependencies:
                result.append(Project.Dependency.from_json(dependency))
            return result

        @staticmethod
        def get(id_: str) -> "Project.Version":
            """Gets a version.

            Args:
                id_ (str): The version ID to find.

            Raises:
                NotFoundError: The version was not found.
                InvalidRequestError: An invalid API call was sent.

            Returns:
                Project.Version: The version that was found.
            """
            raw_response = r.get(
                f"https://api.modrinth.com/v2/version/{id_}", timeout=60
            )
            if raw_response.status_code == 404:
                raise exceptions.NotFoundError(
                    "The requested version was not found or no authorization to see this version"
                )
            if not raw_response.ok:
                raise exceptions.InvalidRequestError()
            response = json.loads(raw_response.content)
            return Project.Version(response)

        def get_files(self) -> list["Project.File"]:
            """
            Gets a versions files.

            Returns:
                list[File]: The versions files
            """
            result = []
            for file in self.model.files:
                result.append(Project.File.from_json(file))  # type: ignore
            return result

        def download(self, recursive: bool = False) -> None:
            """Downloads this version

            Args:
                recursive (bool): Download dependencies
            """
            files = self.get_files()
            for file in files:
                file_content = r.get(file.url).content
                open(file.filename, "wb").write(file_content)

            if recursive:
                dependencies = self.get_dependencies()
                for dep in dependencies:
                    files = dep.get_version().get_files()
                    for file in files:
                        file_content = r.get(file.url).content
                        open(file.filename, "wb").write(file_content)

        def get_project(self) -> "Project":
            """
            Gets a versions project.

            Returns:
                Project: The versions project
            """
            return modrinth.Modrinth.get_project(self.model.project_id)  # type: ignore

        def get_primary_files(self) -> list["Project.File"]:
            """
            Gets a dependencies primary files.

            Returns:
                list[Project.File]: The dependencies primary files
            """
            result = []
            for file in self.get_files():
                if file.primary:
                    result.append(file)
            return result

        def get_author(self) -> object:
            """
            Gets the user who published the version.

            Returns:
                User: The user who published the version
            """
            user = users.User.get(
                self.model.author_id)  # type: ignore
            return user

        def is_featured(self) -> bool:
            """
            Checks if the version is featured.

            Returns:
                bool: If the version is featured
            """
            return self.model.featured

        def get_date_published(self) -> datetime.datetime:
            """
            Gets the date of when the version was published.

            Returns:
                datetime: The date of when the version was published
            """
            return util.format_time(self.model.date_published)

        def get_downloads(self) -> int:
            """
            Gets how many downloads the version has.

            Returns:
                int: The amount of downloads
            """
            return self.model.downloads  # type: ignore

        def get_name(self) -> str:
            """
            Gets the versions name.

            Returns:
                str: The version name
            """
            return self.model.name

        def get_version_number(self) -> str:
            """
            Gets the versions number.

            Returns:
                str: The semantic version number
            """
            return self.model.version_number

        def __repr__(self) -> str:
            return f"Version: {self.model.name}"

    class GalleryImage:
        """Used for a projects gallery images."""

        def __init__(
            self,
            file_path: str,
            featured: bool,
            title: str,
            description,
            ordering: int = 0,
        ) -> None:
            self.file_path = file_path
            self.ext = file_path.split(".")[-1]
            self.featured = str(featured).lower()
            self.title = title
            self.description = description
            self.ordering = ordering

        @staticmethod
        def from_json(json_: dict) -> "Project.GalleryImage":
            """Utility Function."""
            result = Project.GalleryImage(
                json_.get("url"),  # type: ignore
                json_.get("featured"),  # type: ignore
                json_.get("title"),  # type: ignore
                json_.get("description"),  # type: ignore
                json_.get("ordering"),  # type: ignore
            )

            return result

        def to_json(self) -> dict:
            """Utility Function."""
            result = {
                "ext": self.ext,
                "featured": self.featured,
                "title": self.title,
                "description": self.description,
                "ordering": self.ordering,
            }
            result = util.remove_null_values(result)
            return result

    class File:
        """Used for a projects files."""

        def __init__(
            self,
            hashes: dict[str, str],
            url: str,
            filename: str,
            primary: str,
            size: int,
            file_type: str,
        ) -> None:
            self.hashes = hashes
            self.url = url
            self.filename = filename
            self.primary = primary
            self.size = size
            self.file_type = file_type
            self.extension = filename.split(".")[-1]

        def is_resourcepack(self) -> bool:
            """
            Checks if a file is a resourcepack.

            Returns:
                bool: If the file is a resourcepack
            """
            if self.file_type is None:
                return False
            return True

        @staticmethod
        def from_json(json_: dict) -> "Project.File":
            """Utility Function."""
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
            return f"File: {self.filename}"

    class License:
        """Used for a projects license."""

        def __init__(
            self, id_: str, name: str, url: typing.Optional[str] = None
        ) -> None:
            self.id = id_
            self.name = name
            self.url = url

        @staticmethod
        def from_json(json_: dict) -> "Project.License":
            """Utility Function."""
            result = Project.License(
                json_.get("id"), json_.get(
                    "name"), json_.get("url")  # type: ignore
            )

            return result

        def to_json(self) -> dict:
            """Utility Function."""
            result = {"id": self.id, "name": self.name, "url": self.url}

            return result

        def __repr__(self) -> str:
            return f"License: {self.name if self.name else self.id}"

    class Donation:
        """Used for a projects donations."""

        def __init__(self, id_: str, platform: str, url: str) -> None:
            self.id = id_
            self.platform = platform
            self.url = url

        @staticmethod
        def from_json(json_: dict) -> "Project.Donation":
            """Utility Function."""
            result = Project.Donation(json_.get("id"), json_.get(
                "platform"), json_.get("url"))  # type: ignore

            return result

        def __repr__(self) -> str:
            return f"Donation: {self.platform}"

    class Dependency:
        """Used for a projects dependencies."""

        def __init__(self, dependency_type, id_, dependency_option) -> None:
            self.dependency_type = dependency_type
            self.id = id_
            if dependency_type == "project":
                self.id = Project.get(self.id).get_id()
            self.dependency_option = dependency_option

        def to_json(self) -> dict:
            """Utility Function."""
            result = {
                "version_id": None,
                "project_id": None,
                "file_name": None,
                "dependency_type": self.dependency_option,
            }
            if self.dependency_type == "project":
                result.update({"project_id": self.id})
            elif self.dependency_type == "version":
                result.update({"version_id": self.id})
            return result

        @staticmethod
        def from_json(json_: dict) -> "Project.Dependency":
            """Utility Function."""
            dependency_type = "project"
            id_ = json_.get("project_id")
            if json_.get("version_id"):
                dependency_type = "version"
                id_ = json_.get("version_id")

            result = Project.Dependency(
                dependency_type, id_, json_.get("dependency_type")
            )

            return result

        def get_project(self) -> "Project":
            """
            Used to get the project of the dependency.

            Returns:
                Project: The dependency project
            """
            return Project.get(self.id)

        def get_version(self) -> "Project.Version":
            """Gets the dependencies project version."""
            if self.dependency_type == "version":
                return Project.Version.get(self.id)
            project = Project.get(self.id)
            return project.get_latest_version()

        def is_required(self) -> bool:
            """
            Checks if the dependency is required.

            Returns:
                bool: If the dependency is required
            """
            return True if self.dependency_option == "required" else False

        def is_optional(self) -> bool:
            """
            Checks if the dependency is optional.

            Returns:
                bool: If the dependency is optional
            """
            return True if self.dependency_option == "optional" else False

        def is_incompatible(self) -> bool:
            """
            Checks if the dependency is incompatible.

            Returns:
                bool: If the dependency is incompatible
            """
            return True if self.dependency_option == "incompatible" else False

    class SearchResult:
        """A search result from using Modrinth.search_projects()."""

        def __init__(self, search_result_model) -> None:
            if isinstance(search_result_model, dict):
                search_result_model = models.SearchResultModel.from_json(
                    search_result_model
                )
            self.model = search_result_model

        def __repr__(self) -> str:
            return f"Search Result: {self.model.title}"
