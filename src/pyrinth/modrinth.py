"""The main Modrinth class used for anything modrinth related."""

import json
from typing import Optional
import requests as r
from pyrinth.exceptions import InvalidRequestError, NotFoundError
from pyrinth.projects import Project
from pyrinth.users import User


class Modrinth:
    """The main Modrinth class used for anything modrinth related."""

    @staticmethod
    def get_project(id_: str, auth: Optional[str] = None) -> 'Project':
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
            f'https://api.modrinth.com/v2/project/{id_}',
            headers={
                'authorization': auth  # type: ignore
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
        response.update({"authorization": auth})
        return Project(response)

    @staticmethod
    def project_exists(id: str) -> bool:
        """Checks if a project exists.

        Args:
            id (str): The project ID to check if it exists.

        Raises:
            InvalidRequestError: An invalid API call was sent.

        Returns:
            bool: If the project exists.
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id}/check',
            timeout=60
        )
        if not raw_response.ok:
            raise InvalidRequestError()
        response = json.loads(raw_response.content)
        return bool(response['id'])

    @staticmethod
    def get_projects(ids: list[str]) -> list['Project']:
        """Gets multiple projects.

        Raises:
            InvalidRequestError: An invalid API call was sent.

        Returns:
            list[Project]: The projects that were found.
        """
        raw_response = r.get(
            'https://api.modrinth.com/v2/projects',
            params={
                'ids': json.dumps(ids)
            },
            timeout=60
        )
        if not raw_response.ok:
            raise InvalidRequestError()
        response = json.loads(raw_response.content)
        return [Project(project) for project in response]

    @staticmethod
    def get_version(id_: str) -> 'Project.Version':
        """Gets a version.

        Args:
            id (str): The version ID to find.

        Raises:
            NotFoundError: The version was not found.
            InvalidRequestError: An invalid API call was sent.

        Returns:
            Project.Version: The version that was found.
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/version/{id_}',
            timeout=60
        )
        if raw_response.status_code == 404:
            raise NotFoundError(
                "The requested version was not found or no authorization to see this version"
            )
        if not raw_response.ok:
            raise InvalidRequestError()
        response = json.loads(raw_response.content)
        return Project.Version(response)

    @staticmethod
    def get_random_projects(count: int = 1) -> list['Project']:
        """Gets a certain amount of random projects.

        Args:
            count (int, optional): The amount of projects to find. Defaults to 1.

        Raises:
            InvalidRequestError: An invalid API call was sent.

        Returns:
            list[Project]: The projects that were randomly found.
        """
        raw_response = r.get(
            'https://api.modrinth.com/v2/projects_random',
            params={
                'count': count
            },
            timeout=60
        )
        if not raw_response.ok:
            raise InvalidRequestError()
        response = json.loads(raw_response.content)
        return [Project(project) for project in response]

    @staticmethod
    def get_user(id_: str, auth: Optional[str] = None) -> 'User':
        """Gets a user.

        Args:
            id_ (str): The user's ID to find.
            auth (str, optional): The authorization token to use when creating the user. Defaults to None.

        Raises:
            NotFoundError: The user was not found.
            InvalidRequestError: An invalid API call was sent.

        Returns:
            User: The user that was found.
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/user/{id_}',
            timeout=60
        )

        if raw_response.status_code == 404:
            raise NotFoundError("The requested user was not found")

        if not raw_response.ok:
            raise InvalidRequestError()

        response = raw_response.json()
        response.update({"authorization": auth})
        return User(response)

    @staticmethod
    def get_user_from_auth(auth: str) -> 'User':
        """Gets a user from an authorization token.

        Args:
            auth (str): The authorization token to use when finding the user.

        Returns:
            User: The user that was found.
        """
        return User.from_auth(auth)

    @staticmethod
    def search_projects(
        query: str = '', facets: Optional[list[list[str]]] = None,
        index: str = "relevance", offset: int = 0,
        limit: int = 10, filters: Optional[list[str]] = None
    ) -> list['SearchResult']:
        """Searches projects on modrinth

        Raises:
            InvalidRequestError: An invalid API call was sent.

        Returns:
            list[SearchResult]: The results that were found.
        """
        params = {}
        if query != '':
            params.update({'query': query})
        if facets:
            params.update({'facets': json.dumps(facets)})
        if index != 'relevance':
            params.update({'index': index})
        if offset != 0:
            params.update({'offset': str(offset)})
        if limit != 10:
            params.update({'limit': str(limit)})
        if filters:
            params.update({'filters': json.dumps(filters)})
        raw_response = r.get(
            'https://api.modrinth.com/v2/search',
            params=params,
            timeout=60
        )
        if not raw_response.ok:
            raise InvalidRequestError()
        response = json.loads(raw_response.content)
        return [Modrinth.SearchResult(project) for project in response['hits']]

    class SearchResult:
        """A search result from using Modrinth.search_projects()."""

        def __init__(self, search_result_model) -> None:
            from pyrinth.models import SearchResultModel
            if isinstance(search_result_model, dict):
                search_result_model = SearchResultModel.from_json(
                    search_result_model
                )
            self.model = search_result_model

        def __repr__(self) -> str:
            return f"Search Result: {self.model.title}"

    class Statistics:
        """Modrinth statistics."""

        def __init__(self) -> None:
            raw_response = r.get(
                'https://api.modrinth.com/v2/statistics',
                timeout=60
            )
            response = json.loads(raw_response.content)
            self.authors = response['authors']
            self.files = response['files']
            self.projects = response['projects']
            self.versions = response['versions']
