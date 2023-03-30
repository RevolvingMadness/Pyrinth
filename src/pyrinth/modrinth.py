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
        """
        Gets a project based on an ID.

        Returns:
            Project: The project that was found using the ID
            None: If no project was found
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
    def exists(project_id: str) -> bool:
        """
        Checks if a project exists.

        Returns:
            bool: If the project exists
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{project_id}/check',
            timeout=60
        )
        if raw_response.status_code == 404:
            raise NotFoundError("The requested project was not found")
        if not raw_response.ok:
            raise InvalidRequestError()
        response = json.loads(raw_response.content)
        return bool(response['id'])

    @staticmethod
    def get_projects(ids: list[str]) -> list['Project']:
        """
        Gets a list of projects based on IDs.

        Returns:
            list[Project]: The projects that were found using the IDs
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
        """
        Gets a version based on an ID.

        Returns:
            Project.Version: The version that was found using the ID
            None: If no version was found
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
        """
        Gets an amount of random projects.

        Args:
            count (int, optional): The amount of random projects to return. Defaults to 1.

        Returns:
            list[Project]: The amount of random projects that were found
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
        """
        Gets a user.

        Returns
            User: The user that was found using the ID
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
        """
        Gets a user from authorization token.

        Returns:
            User: The user that was found using the authorization token
            None: No user was found
        """
        return User.from_auth(auth)

    @staticmethod
    def search_projects(
        query: str = '', facets: Optional[list[list[str]]] = None,
        index: str = "relevance", offset: int = 0,
        limit: int = 10, filters: Optional[list[str]] = None
    ) -> list['SearchResult']:
        """
        Searches for projects using 6 arguments.

        Returns:
            list[Modrinth.SearchResult]: The projects that were found using the 6 arguments
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
