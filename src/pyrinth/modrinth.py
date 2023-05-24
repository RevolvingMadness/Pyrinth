import requests as _requests
import pyrinth.exceptions as _exceptions
import pyrinth.projects as _projects


class Modrinth:
    @staticmethod
    def project_exists(id_: str) -> bool:
        """Checks if a project exists

        Args:
            id_ (str): The ID or slug of the project

        Raises:
            InvalidRequestError: Invalid request
            NotFoundError: The requested project was not found

        Returns:
            (bool): Whether the project exists
        """
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/project/{id_}/check", timeout=60
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError("The requested project was not found")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return response.get("id", False)

    @staticmethod
    def get_random_projects(count: int = 1) -> list["_projects.Project"]:
        """Gets a certain number of random projects

        Args:
            count (int, optional): The number of random projects to return

        Raises:
            (src.pyrinth.exceptions.InvalidRequestError): Invalid request

        Returns:
            (list[Project]): The projects that were randomly found
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/projects_random",
            params={"count": count},
            timeout=60,
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response = raw_response.json()
        return [_projects.Project(project) for project in response]

    @property
    def statistics(self) -> "Modrinth._Statistics":
        return Modrinth._Statistics()

    class _Statistics:
        """Modrinth statistics

        Attributes:
            authors (int, optional): The number of authors on Modrinth
            files (int, optional): The number of files on Modrinth
            projects (int, optional): The number of projects on Modrinth
            versions (int, optional): The number of versions on Modrinth

        """

        @classmethod
        @property
        def authors(self) -> None:
            raw_response = _requests.get(
                "https://api.modrinth.com/v2/statistics", timeout=60
            )
            response: dict = raw_response.json()
            return response.get("authors")

        @classmethod
        @property
        def files(self) -> None:
            raw_response = _requests.get(
                "https://api.modrinth.com/v2/statistics", timeout=60
            )
            response: dict = raw_response.json()
            return response.get("files")

        @classmethod
        @property
        def projects(self) -> None:
            raw_response = _requests.get(
                "https://api.modrinth.com/v2/statistics", timeout=60
            )
            response: dict = raw_response.json()
            return response.get("projects")

        @classmethod
        @property
        def versions(self) -> None:
            raw_response = _requests.get(
                "https://api.modrinth.com/v2/statistics", timeout=60
            )
            response: dict = raw_response.json()
            return response.get("versions")
