"""
User projects
"""

from datetime import datetime
from typing import Optional, Union
import json
import requests as r
from pyrinth.exceptions import InvalidParamError, InvalidRequestError, NoAuthorization, NotFoundError
from pyrinth.util import remove_null_values


class Project:
    """
    Contains information about a users projects
    """

    def __init__(self, project_model) -> None:
        from pyrinth.models import ProjectModel
        if isinstance(project_model, dict):
            project_model = ProjectModel.from_json(project_model)
        self.project_model = project_model

    def __repr__(self) -> str:
        return f"Project: {self.project_model.title}"

    @staticmethod
    def get(id_: str, auth: str = '') -> 'Project':
        """Alternative method for Modrinth.get_project(id_, auth)"""
        from pyrinth.modrinth import Modrinth
        return Modrinth.get_project(id_, auth)

    def get_latest_version(
        self, loaders: Optional[list[str]] = None,
        game_versions: Optional[list[str]] = None,
        featured: Optional[bool] = None,
        types: Optional[list[str]] = None,
        auth: str = ''
    ) -> 'Project.Version':
        """Gets the latest project version

        Returns:
            Project.Version: The latest project version
        """
        versions = self.get_versions(
            loaders, game_versions, featured, types, auth
        )

        return versions[0]

    def is_client_side(self) -> bool:
        """Checks if this project is client side"""
        return (True if self.project_model.client_side == 'required' else False)

    def is_server_side(self) -> bool:
        """Checks if this project is server side"""
        return (True if self.project_model.server_side == 'required' else False)

    def get_downloads(self) -> int:
        """Gets the amount of downloads this project has"""
        return self.project_model.downloads

    def get_categories(self) -> list[str]:
        """Gets this projects categories"""
        return self.project_model.categories

    def get_additional_categories(self) -> list[str]:
        """Gets this projects additional categories"""
        return self.project_model.additional_categories

    def get_all_categories(self) -> list[str]:
        """Gets this projects categories and additional categories"""
        return self.get_categories() + self.get_additional_categories()

    def get_license(self) -> 'Project.License':
        """Gets this projects license"""
        return Project.License.from_json(self.project_model.license)

    def get_specific_version(self, semantic_version: str) -> Union['Project.Version', None]:
        """Gets a specific project version based on the semantic version

        Returns:
            Project.Version: The version that was found using the semantic version
        """
        versions = self.get_versions()
        if versions:
            for version in versions:
                if version.version_model.version_number == semantic_version:
                    return version

        return None

    def get_versions(
        self, loaders: Optional[list[str]] = None,
        game_versions: Optional[list[str]] = None,
        featured: Optional[bool] = None,
        types: Optional[list[str]] = None,
        auth: str = ''
    ) -> list['Project.Version']:
        """Gets project versions based on filters

        Returns:
            list[Project.Version]: The versions that were found using the filters
        """
        from pyrinth.util import json_to_query_params
        filters = {
            'loaders': loaders,
            'game_versions': game_versions,
            'featured': featured
        }

        filters = remove_null_values(filters)
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/version',
            params=json_to_query_params(filters),
            headers={
                'authorization': auth
            },
            timeout=60
        )

        if raw_response.status_code == 404:
            raise NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = json.loads(raw_response.content)

        versions = [self.Version(version) for version in response]

        if not types:
            return versions

        result = []
        for version in versions:
            if version.version_model.version_type in types:
                result.append(version)

        return result

    def get_oldest_version(
        self, loaders: Optional[list[str]] = None,
        game_versions: Optional[list[str]] = None,
        featured: Optional[bool] = None,
        types: Optional[list[str]] = None,
        auth: str = ''
    ) -> 'Project.Version':
        """Gets the oldest project version

        Returns:
            Project.Version: The oldest project version
        """
        versions = self.get_versions(
            loaders, game_versions, featured, types, auth
        )

        return versions[-1]

    def get_id(self) -> str:
        """Gets the ID of the project

        Returns:
            str: The ID of the project
        """
        return self.project_model.id

    def get_slug(self) -> str:
        """Gets the slug of the project

        Returns:
            str: The slug of the project
        """
        return self.project_model.slug

    def get_name(self) -> str:
        """Gets the name of the project

        Returns:
            str: The name of the project
        """
        return self.project_model.title

    @staticmethod
    def get_version(id_: str) -> 'Project.Version':
        """Gets a version by ID

        Returns:
            Project.Version: The version that was found using the ID
            None: The version was not found
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/version/{id_}',
            timeout=60
        )

        if raw_response.status_code == 404:
            raise NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = json.loads(raw_response.content)
        return Project.Version(response)

    def create_version(self, auth: str, version_model) -> int:
        """Creates a new version on the project

        Args:
            auth (str): The authorization token to use when creating a version
            version_model (VersionModel): The VersionModel to use for the new project version

        Returns:
            int: If creating the new project version was successful
        """
        from pyrinth.util import remove_file_path
        version_model.project_id = self.project_model.id

        files = {
            "data": version_model.to_bytes()
        }

        for file in version_model.files:
            files.update({remove_file_path(file): open(file, "rb").read()})

        raw_response = r.post(
            'https://api.modrinth.com/v2/version',
            headers={
                "authorization": auth
            },
            files=files,
            timeout=60
        )

        if raw_response.status_code == 401:
            raise NoAuthorization("No authorization to create this version")

        if not raw_response.ok:
            raise InvalidRequestError()

        return 1

    def change_icon(self, file_path: str, auth: str) -> int:
        """Changes the projects icon

        Args:
            file_path (str): The file path of the image to use for the new project icon
            auth (str): The authorization token to use when changing the projects icon

        Returns:
            int: If the project icon change was successful
        """
        raw_response = r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/icon',
            params={
                "ext": file_path.split(".")[-1]
            },
            headers={
                "authorization": auth
            },
            data=open(file_path, "rb"),
            timeout=60
        )

        if raw_response.status_code == 400:
            raise InvalidParamError("Invalid input for new icon")

        if not raw_response.ok:
            raise InvalidRequestError()

        return 1

    def delete_icon(self, auth: str) -> int:
        """Deletes the projects icon

        Args:
            auth (str): The authorization token to use when deleting the projects icon

        Returns:
            int: If the project icon deletion was successful
        """
        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/icon',
            headers={
                "authorization": auth
            },
            timeout=60
        )

        if raw_response.status_code == 400:
            raise InvalidParamError("Invalid input")

        if raw_response.status_code == 401:
            raise NoAuthorization("No authorization to edit this project")

        if not raw_response.ok:
            raise InvalidRequestError()

        return 1

    def add_gallery_image(self, auth: str, image: 'Project.GalleryImage') -> int:
        """Adds a gallery image to the project

        Args:
            auth (str): The authorization token to use when adding the gallery image
            image (Project.GalleryImage): The gallery image to add

        Returns:
            int: If the gallery image addition was successful
        """
        raw_response = r.post(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery',
            headers={
                "authorization": auth
            },
            params=image.to_json(),
            data=open(image.file_path, "rb"),
            timeout=60
        )

        if raw_response.status_code == 401:
            raise NoAuthorization("No authorization to create a gallery image")

        if raw_response.status_code == 404:
            raise NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise InvalidRequestError()

        return 1

    def modify_gallery_image(
        self, auth: str, url: str, featured: Optional[bool] = None,
        title: Optional[str] = None, description: Optional[str] = None,
        ordering: Optional[int] = None
    ) -> int:
        """Modifies a project gallery image

        Args:
            auth (str): The authorization token to use when modifying the gallery image
            url (str): The url of the gallery image
            featured (Optional[bool], optional): If the new gallery image is featured. Defaults to None.
            title (Optional[str], optional): The new gallery image title. Defaults to None.
            description (Optional[str], optional): The new gallery image description. Defaults to None.
            ordering (Optional[int], optional): The new gallery image ordering. Defaults to None.

        Returns:
            int: If the gallery image modification was successful
        """
        modified_json = {
            'url': url,
            'featured': featured,
            'title': title,
            'description': description,
            'ordering': ordering
        }

        modified_json = remove_null_values(modified_json)

        raw_response = r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery',
            params=modified_json,
            headers={
                'authorization': auth
            },
            timeout=60
        )

        if raw_response.status_code == 401:
            raise NoAuthorization(
                "No authorization to edit this gallery image")

        if raw_response.status_code == 404:
            raise NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise InvalidRequestError()

        return 1

    def delete_gallery_image(self, url: str, auth: str) -> int:
        """Deletes a projects gallery image

        Args:
            url (str): The url of the gallery image
            auth (str): The authorization token to use when deleting the gallery image

        Raises:
            Exception: If the user used cdn-raw.modrinth.com instead of cdn.modrinth.com

        Returns:
            int: If the gallery image deletion was successful
        """
        if '-raw' in url:
            raise InvalidParamError(
                "Please use cdn.modrinth.com instead of cdn-raw.modrinth.com"
            )

        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery',
            headers={
                "authorization": auth
            },
            params={
                "url": url
            },
            timeout=60
        )

        if raw_response.status_code == 400:
            raise InvalidParamError("Invalid URL or project specified")

        if raw_response.status_code == 401:
            raise NoAuthorization(
                "No authorization to delete this gallery image"
            )

        if not raw_response.ok:
            raise InvalidRequestError()

        return 1

    def modify(
        self, auth: str, slug: Optional[str] = None, title: Optional[str] = None,
        description: Optional[str] = None, categories: Optional[list[str]] = None,
        client_side: Optional[str] = None, server_side: Optional[str] = None,
        body: Optional[str] = None, additional_categories: Optional[list[str]] = None,
        issues_url: Optional[str] = None, source_url: Optional[str] = None,
        wiki_url: Optional[str] = None, discord_url: Optional[str] = None,
        license_id: Optional[str] = None, license_url: Optional[str] = None,
        status: Optional[str] = None, requested_status: Optional[str] = None,
        moderation_message: Optional[str] = None, moderation_message_body: Optional[str] = None
    ) -> int:
        """Modifies a project

        Args:
            auth (str): The authorization token to use to modify the project
            slug (Optional[str], optional): The new project slug. Defaults to None.
            title (Optional[str], optional): The new project title. Defaults to None.
            description (Optional[str], optional): The new project description. Defaults to None.
            categories (Optional[list[str]], optional): The new project categories. Defaults to None.
            client_side (Optional[str], optional): If the project is supported on client_side. Defaults to None.
            server_side (Optional[str], optional): If the project is supported on the server side. Defaults to None.
            body (Optional[str], optional): The new project body. Defaults to None.
            additional_categories (Optional[list[str]], optional): The new project additional categories. Defaults to None.
            issues_url (Optional[str], optional): The new project issues url. Defaults to None.
            source_url (Optional[str], optional): The new project source url. Defaults to None.
            wiki_url (Optional[str], optional): The new project wiki url. Defaults to None.
            discord_url (Optional[str], optional): The new project discord url. Defaults to None.
            license_id (Optional[str], optional): The new project license id. Defaults to None.
            license_url (Optional[str], optional): The new project license url. Defaults to None.
            status (Optional[str], optional): The new project status. Defaults to None.
            requested_status (Optional[str], optional): The new project requested status. Defaults to None.
            moderation_message (Optional[str], optional): The new project moderation message. Defaults to None.
            moderation_message_body (Optional[str], optional): The new project moderation message body. Defaults to None.

        Raises:
            Exception: If no new project arguments are specified

        Returns:
            int: If the project modification was successful
        """
        modified_json = {
            'slug': slug,
            'title': title,
            'description': description,
            'categories': categories,
            'client_side': client_side,
            'server_side': server_side,
            'body': body,
            'additional_categories': additional_categories,
            'issues_url': issues_url,
            'source_url': source_url,
            'wiki_url': wiki_url,
            'discord_url': discord_url,
            'license_id': license_id,
            'license_url': license_url,
            'status': status,
            'requested_status': requested_status,
            'moderation_message': moderation_message,
            'moderation_message_body': moderation_message_body
        }

        modified_json = remove_null_values(modified_json)

        if not modified_json:
            raise InvalidParamError(
                "Please specify at least 1 optional argument.")

        raw_response = r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}',
            data=json.dumps(modified_json),
            headers={
                'Content-Type': 'application/json',
                'authorization': auth
            },
            timeout=60
        )

        if raw_response.status_code == 401:
            raise NoAuthorization("No authorization to edit this project")

        if raw_response.status_code == 404:
            raise NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise InvalidRequestError()

        return 1

    def delete(self, auth: str) -> int:
        """Deletes the project

        Args:
            auth (str): The authorization token to delete the project

        Returns:
            int: If the deletion was successful
        """
        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}',
            headers={
                'authorization': auth
            },
            timeout=60
        )

        if raw_response.status_code == 400:
            raise NotFoundError("The requested project was not found")

        if raw_response.status_code == 401:
            raise NoAuthorization("No authorization to delete this project")

        if not raw_response.ok:
            raise InvalidRequestError()

        return 1

    def get_dependencies(self) -> list['Project']:
        """Gets a projects dependencies

        Returns:
            list[Project]: The projects dependencies
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/dependencies',
            timeout=60
        )

        if raw_response.status_code == 404:
            raise NotFoundError(
                "The requested project was not found or no authorization to see this project"
            )

        if not raw_response.ok:
            raise InvalidRequestError()

        response = json.loads(raw_response.content)
        return [Project(dependency) for dependency in response['projects']]

    class Version:
        """Used for a projects versions
        """

        def __init__(self, version_model) -> None:
            from pyrinth.models import VersionModel
            if isinstance(version_model, dict):
                version_model = VersionModel.from_json(version_model)
                self.version_model = version_model
            self.version_model = version_model

        def get_type(self):
            """Gets the versions type (release / beta / alpha)"""
            return self.version_model.version_type

        def get_dependencies(self) -> list['Project.Dependency']:
            """Gets a projects dependencies

            Returns:
                list[Project.Dependency]: The projects dependencies
            """
            result = []
            for dependency in self.version_model.dependencies:
                result.append(Project.Dependency.from_json(dependency))
            return result

        def get_files(self) -> list['Project.File']:
            """Gets a versions files

            Returns:
                list[Project.File]: The versions files
            """
            result = []
            for file in self.version_model.files:
                result.append(Project.File.from_json(file))
            return result

        def get_project(self) -> 'Project':
            """Gets a versions project

            Returns:
                Project: The versions project
            """
            from pyrinth.modrinth import Modrinth
            return Modrinth.get_project(self.version_model.project_id)

        def get_primary_files(self) -> list['Project.File']:
            """Gets a dependencies primary files

            Returns:
                list[Project.File]: The dependencies primary files
            """
            result = []
            for file in self.get_files():
                if file.primary:
                    result.append(file)
            return result

        def get_author(self) -> object:
            """Gets the user who published the version

            Returns:
                User: The user who published the version
            """
            from pyrinth.modrinth import Modrinth
            user = Modrinth.get_user(self.version_model.author_id)
            return user

        def is_featured(self) -> bool:
            """Checks if the version is featured

            Returns:
                bool: If the version is featured
            """
            return self.version_model.featured

        def get_date_published(self) -> datetime:
            """Gets the date of when the version was published

            Returns:
                datetime: The date of when the version was published
            """
            from pyrinth.util import format_time
            return format_time(self.version_model.date_published)

        def get_downloads(self) -> int:
            """Gets how many downloads the version has

            Returns:
                int: The amount of downloads
            """
            return self.version_model.downloads

        def get_name(self) -> str:
            """Gets the versions name

            Returns:
                str: The version name
            """
            return self.version_model.name

        def get_version_number(self) -> str:
            """Gets the versions number

            Returns:
                str: The semantic version number
            """
            return self.version_model.version_number

        def __repr__(self) -> str:
            return f"Version: {self.version_model.name}"

    class GalleryImage:
        """Used for a projects gallery images
        """

        def __init__(
            self, file_path: str, featured: bool,
            title: str, description, ordering: int = 0
        ) -> None:
            self.file_path = file_path
            self.ext = file_path.split(".")[-1]
            self.featured = str(featured).lower()
            self.title = title
            self.description = description
            self.ordering = ordering

        @staticmethod
        def from_json(json_: dict) -> 'Project.GalleryImage':
            """Utility Function"""
            result = Project.GalleryImage(
                json_['url'], json_['featured'], json_['title'],
                json_['description'], json_['ordering']
            )

            return result

        def to_json(self) -> dict:
            """Utility Function"""
            result = {
                "ext": self.ext,
                "featured": self.featured,
                "title": self.title,
                "description": self.description,
                "ordering": self.ordering
            }
            result = remove_null_values(result)
            return result

    class File:
        """Used for a projects files
        """

        def __init__(
            self, hashes: dict[str, str], url: str, filename: str,
            primary: str, size: int, file_type: str
        ) -> None:
            self.hashes = hashes
            self.url = url
            self.filename = filename
            self.primary = primary
            self.size = size
            self.file_type = file_type
            self.extension = filename.split('.')[-1]

        def is_resourcepack(self) -> bool:
            """Checks if a file is a resourcepack

            Returns:
                bool: If the file is a resourcepack
            """
            if self.file_type is None:
                return False
            return True

        @staticmethod
        def from_json(json_: dict) -> 'Project.File':
            """Utility Function"""
            result = Project.File(
                json_['hashes'],
                json_['url'],
                json_['filename'],
                json_['primary'],
                json_['size'],
                json_['file_type']
            )
            return result

        def __repr__(self) -> str:
            return f"File: {self.filename}"

    class License:
        """Used for a projects license
        """

        def __init__(self, id_: str, name: str, url: str) -> None:
            self.id = id_
            self.name = name
            self.url = url

        @staticmethod
        def from_json(json_: dict) -> 'Project.License':
            """Utility Function"""
            result = Project.License(
                json_['id'],
                json_['name'],
                json_['url']
            )

            return result

        def to_json(self) -> dict:
            """Utility Function"""
            result = {
                'id': self.id,
                'name': self.name,
                'url': self.url
            }

            return result

        def __repr__(self) -> str:
            return f"License: {self.name if self.name else self.id}"

    class Donation:
        """Used for a projects donations
        """

        def __init__(self, id_: str, platform: str, url: str) -> None:
            self.id = id_
            self.platform = platform
            self.url = url

        @staticmethod
        def from_json(json_: dict) -> 'Project.Donation':
            """Utility Function"""
            result = Project.Donation(
                json_['id'],
                json_['platform'],
                json_['url']
            )

            return result

        def __repr__(self) -> str:
            return f"Donation: {self.platform}"

    class Dependency:
        """Used for a projects dependencies
        """

        def __init__(self, dependency_type, id_, dependency_option):
            from pyrinth.modrinth import Modrinth
            self.dependency_type = dependency_type
            self.id = id_
            if dependency_type == "project":
                self.id = Modrinth.get_project(self.id).get_id()
            self.dependency_option = dependency_option

        def to_json(self):
            """Utility Function"""
            result = {
                "version_id": None,
                "project_id": None,
                "file_name": None,
                "dependency_type": self.dependency_option
            }
            if self.dependency_type == "project":
                result.update({"project_id": self.id})
            elif self.dependency_type == "version":
                result.update({"version_id": self.id})
            return result

        @staticmethod
        def from_json(json_: dict) -> 'Project.Dependency':
            """Utility Function"""
            dependency_type = "project"
            id_ = json_['project_id']
            if json_['version_id']:
                dependency_type = "version"
                id_ = json_['version_id']

            result = Project.Dependency(
                dependency_type,
                id_,
                json_['dependency_type']
            )

            return result

        def get_project(self) -> 'Project':
            """Used to get the project of the dependency

            Returns:
                Project: The dependency project
            """
            from pyrinth.modrinth import Modrinth
            return Modrinth.get_project(self.id)

        def get_version(self) -> 'Project.Version':
            """Gets the dependencies project version
            """
            from pyrinth.modrinth import Modrinth
            if self.dependency_type == "version":
                return Modrinth.get_version(self.id)
            project = Modrinth.get_project(self.id)
            return project.get_latest_version()

        def is_required(self) -> bool:
            """Checks if the dependency is required

            Returns:
                bool: If the dependency is required
            """
            return (True if self.dependency_option == "required" else False)

        def is_optional(self) -> bool:
            """Checks if the dependency is optional

            Returns:
                bool: If the dependency is optional
            """
            return (True if self.dependency_option == "optional" else False)

        def is_incompatible(self) -> bool:
            """Checks if the dependency is incompatible

            Returns:
                bool: If the dependency is incompatible
            """
            return (True if self.dependency_option == "incompatible" else False)
