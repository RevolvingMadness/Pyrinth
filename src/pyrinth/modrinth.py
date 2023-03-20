"""
The main Modrinth class used for anything modrinth related
"""

from typing import Union
import json
import requests as r
from pyrinth.projects import Project
from pyrinth.users import User


class Modrinth:
    def __init__(self) -> None:
        raise Exception("This class cannot be initalized!")

    @staticmethod
    def get_project(id_: str, auth: str = '') -> Union['Project', None]:
        """Gets a project based on an ID

        Returns:
            Project: The project that was found using the ID
            None: If no project was found
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id_}',
            headers={
                'authorization': auth
            }
        )
        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content!r}")
            return None
        response = json.loads(raw_response.content)
        return Project(response)

    @staticmethod
    def exists(project_id: str) -> bool:
        """Checks if a project exists

        Returns:
            bool: If the project exists
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{project_id}/check'
        )

        response = json.loads(raw_response.content)
        return bool(response['id'])

    @staticmethod
    def get_projects(ids: list[str]) -> list['Project']:
        """Gets a list of projects based on IDs

        Returns:
            list[Project]: The projects that were found using the IDs
        """
        raw_response = r.get(
            'https://api.modrinth.com/v2/projects',
            params={
                'ids': json.dumps(ids)
            }
        )
        response = json.loads(raw_response.content)
        return [Project(project) for project in response]

    @staticmethod
    def get_version(id_: str) -> Union['Project.Version', None]:
        """Gets a version based on an ID

        Returns:
            Project.Version: The version that was found using the ID
            None: If no version was found
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/version/{id_}'
        )
        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content!r}")
            return None
        response = json.loads(raw_response.content)
        return Project.Version(response)

    @staticmethod
    def get_random_projects(count: int = 1) -> Union[list['Project'], None]:
        """Gets an amount of random projects

        Args:
            count (int, optional): The amount of random projects to return. Defaults to 1.

        Returns:
            list[Project]: The amount of random projects that were found
        """
        raw_response = r.get(
            'https://api.modrinth.com/v2/projects_random',
            params={
                'count': count
            }
        )
        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content!r}")
            return None
        response = json.loads(raw_response.content)
        return [Project(project) for project in response]

    @staticmethod
    def get_user_from_id(id_: str) -> Union['User', None]:
        """Gets a user from id

        Returns:
            User: The user that was found using the id
            None: No user was found
        """
        return User.from_id(id_)

    @staticmethod
    def get_user_from_auth(auth: str) -> Union['User', None]:
        """Gets a user from authorization token

        Returns:
            User: The user that was found using the authorization token
            None: No user was found
        """
        return User.from_auth(auth)

    @staticmethod
    def search_projects(query: str = '', facets: list[list[str]] = [], index: str = "relevance", offset: int = 0, limit: int = 10, filters: list[str] = []) -> Union[list['Modrinth.SearchResult'], None]:
        """Searches for projects using 6 arguments

        Returns:
            list[Modrinth.SearchResult]: The projects that were found using the 6 arguments
        """
        params = {}
        if query != '':
            params.update({'query': query})
        if facets != []:
            params.update({'facets': json.dumps(facets)})
        if index != 'relevance':
            params.update({'index': index})
        if offset != 0:
            params.update({'offset': str(offset)})
        if limit != 10:
            params.update({'limit': str(limit)})
        if filters != []:
            params.update({'filters': json.dumps(filters)})
        raw_response = r.get(
            'https://api.modrinth.com/v2/search',
            params=params
        )
        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content!r}")
            return None
        response = json.loads(raw_response.content)
        return [Modrinth.SearchResult(project) for project in response['hits']]

    class SearchResult:
        """A search result from using Modrinth.search_projects
        """

        def __init__(self, search_result_model) -> None:
            from pyrinth.models import SearchResultModel
            if isinstance(search_result_model, dict):
                search_result_model = SearchResultModel.from_json(
                    search_result_model
                )
            self.search_result_model = search_result_model

        def __repr__(self) -> str:
            return f"Search Result: {self.search_result_model.title}"

    class Statistics:
        """Modrinth statistics
        """

        def __init__(self) -> None:
            raw_response = r.get(
                'https://api.modrinth.com/v2/statistics'
            )
            response = json.loads(raw_response.content)
            self.authors = response['authors']
            self.files = response['files']
            self.projects = response['projects']
            self.versions = response['versions']
