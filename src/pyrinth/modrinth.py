"""The main Modrinth class used for anything modrinth related."""

import json

import requests as r

import pyrinth.exceptions as exceptions
import pyrinth.projects as projects


class Modrinth:
    """The main Modrinth class used for anything modrinth related."""

    @staticmethod
    def project_exists(id_: str) -> bool:
        """Checks if a project exists.

        Args:
            id_ (str): The project ID to check if it exists.

        Raises:
            InvalidRequestError: An invalid API call was sent.

        Returns:
            (bool): If the project exists.
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/project/{id_}/check", timeout=60
        )
        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)
        response = json.loads(raw_response.content)
        return bool(response.get("id"))

    @staticmethod
    def get_random_projects(count: int = 1) -> list["projects.Project"]:
        """Gets a certain amount of random projects.

        Args:
            count (int, optional): The amount of projects to find.

        Raises:
            InvalidRequestError: An invalid API call was sent.

        Returns:
            (list[Project]): The projects that were randomly found.
        """
        raw_response = r.get(
            "https://api.modrinth.com/v2/projects_random",
            params={"count": count},
            timeout=60,
        )
        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)
        response = json.loads(raw_response.content)
        return [projects.Project(project) for project in response]

    class Statistics:
        """Modrinth statistics.

        Attributes:
            authors (int, optional): The number of authors on Modrinth.
            files (int, optional): The number of files on Modrinth.
            projects (int, optional): The number of projects on Modrinth.
            versions (int, optional): The number of versions on Modrinth.

        """

        def __init__(self) -> None:
            raw_response = r.get("https://api.modrinth.com/v2/statistics", timeout=60)
            response = json.loads(raw_response.content)
            self.authors: int = response.get("authors")
            self.files: int = response.get("files")
            self.projects: int = response.get("projects")
            self.versions: int = response.get("versions")
