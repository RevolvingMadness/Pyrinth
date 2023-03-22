"""
Used for users
"""

from typing import Union
import json
import requests as r
from pyrinth.projects import Project


class User:
    """
    Contains information about users
    """

    def __init__(
        self, username: str, authorization: str = '',
        ignore_warning: bool = False
    ) -> None:
        self.auth = authorization
        if self.auth != '':
            self.raw_response = r.get(
                'https://api.modrinth.com/v2/user',
                headers={
                    'authorization': self.auth
                }
            )
            if not self.raw_response.ok:
                raise Exception("Invalid auth token")

        if self.auth == '':
            self.raw_response = r.get(
                f'https://api.modrinth.com/v2/user/{username}'
            )
            if not ignore_warning:
                print('[WARNING] Some functions won\'t work without an auth key')

        self.response = json.loads(self.raw_response.content)
        self.username = self.response['username']
        self.id = self.response['id']
        self.github_id = self.response['github_id']
        self.name = self.response['name']
        self.email = self.response['email']
        self.avatar_url = self.response['avatar_url']
        self.bio = self.response['bio']
        self.created = self.response['created']
        self.role = self.response['role']
        self.badges = self.response['badges']
        self.payout_data = self.response['payout_data']

    def get_followed_projects(self) -> Union[list['Project'], None]:
        """Gets a users followed projects

        Returns:
            list[Project]: The users followed projects
        """

        raw_response = r.get(
            f'https://api.modrinth.com/v2/user/{self.username}/follows',
            headers={
                'authorization': self.auth
            }
        )

        if not raw_response.ok:
            print(
                f"Invalid Request: {json.loads(raw_response.content)['description']}"
            )
            return None

        followed_projects = []
        projects = json.loads(raw_response.content)
        for project in projects:
            followed_projects.append(Project(project))

        return followed_projects

    def get_notifications(self) -> Union[list['User.Notification'], None]:
        """Gets a users notifications

        Returns:
            list[User.Notification]: The users notifications
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/user/{self.username}/notifications',
            headers={
                'authorization': self.auth
            }
        )

        if not raw_response.ok:
            print(
                f"Invalid Request: {json.loads(raw_response.content)['description']}"
            )
            return None

        response = json.loads(raw_response.content)
        return [User.Notification(notification) for notification in response]

    def get_amount_of_projects(self) -> Union[int, None]:
        """Gets the amount of projects a user has

        Returns:
            list[Project]: The users projects
        """
        projs = self.get_projects()

        if not projs:
            return None

        return len(projs)

    def create_project(self, project_model, icon: str = '') -> Union[int, None]:
        """Creates a project

        Args:
            project_model (ProjectModel): The model of the project to create
            icon (str, optional): The path of the icon to use for the newly created project. NOT IMPLEMENTED

        Returns:
            int: If the project creation was successful
        """
        raw_response = r.post(
            'https://api.modrinth.com/v2/project',
            files={
                "data": project_model.to_bytes()
            },
            headers={
                'authorization': self.auth
            }
        )

        if not raw_response.ok:
            print(
                f"Invalid Request: {json.loads(raw_response.content)['description']}"
            )
            return None

        return 1

    def get_projects(self) -> Union[list['Project'], None]:
        """Gets a users projects

        Returns:
            list[Project]: The users projects
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/user/{self.id}/projects'
        )

        if not raw_response.ok:
            print(
                f"Invalid Request: {json.loads(raw_response.content)['description']}"
            )
            return None

        response = json.loads(raw_response.content)
        return [Project(project) for project in response]

    def follow_project(self, id: str) -> Union[int, None]:
        """Follow a project

        Args:
            id (str): The ID of the project to follow

        Returns:
            int: If the project follow was successful
        """
        raw_response = r.post(
            f'https://api.modrinth.com/v2/project/{id}/follow',
            headers={
                'authorization': self.auth
            }
        )

        if not raw_response.ok:
            print(
                f"Invalid Request: {json.loads(raw_response.content)['description']}"
            )
            return None

        return 1

    def unfollow_project(self, id: str) -> Union[int, None]:
        """Unfollow a project

        Args:
            id (str): The ID of the project to unfollow

        Returns:
            int: If the project unfollow was successful
        """
        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{id}/follow',
            headers={
                'authorization': self.auth
            }
        )

        if not raw_response.ok:
            print(
                f"Invalid Request: {json.loads(raw_response.content)['description']}"
            )
            return None

        return 1

    @staticmethod
    def from_auth(auth: str) -> Union['User', None]:
        """Gets a user from authorization token

        Returns:
            User: The user that was found using the authorization token
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/user',
            headers={
                'authorization': auth
            }
        )

        if not raw_response.ok:
            print(
                f"Invalid Request: {json.loads(raw_response.content)['description']}"
            )
            return None

        response = json.loads(raw_response.content)
        return User(response['username'], auth, ignore_warning=True)

    @staticmethod
    def from_id(id_: str) -> Union['User', None]:
        """Gets a user from ID

        Returns:
            User: The user that was found using the ID
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/user/{id_}'
        )

        if not raw_response.ok:
            print(
                f"Invalid Request: {json.loads(raw_response.content)['description']}"
            )
            return None

        response = json.loads(raw_response.content)
        return User(response['username'], ignore_warning=True)

    @staticmethod
    def from_ids(ids: list[str]) -> list['User']:
        """Gets a users from IDs

        Returns:
            User: The users that were found using the IDs
        """
        raw_response = r.get(
            'https://api.modrinth.com/v2/users',
            params={
                'ids': json.dumps(ids)
            }
        )

        response = json.loads(raw_response.content)
        return [User(user['username']) for user in response]

    class Notification:
        """Used for the users notifications
        """

        def __init__(self, notification_json: dict) -> None:
            self.id = notification_json['id']
            self.user_id = notification_json['user_id']
            self.type = notification_json['type']
            self.title = notification_json['title']
            self.text = notification_json['text']
            self.link = notification_json['link']
            self.read = notification_json['read']
            self.created = notification_json['created']
            self.actions = notification_json['actions']
            self.project_title = self.title.split('**')[1]

        def __repr__(self) -> str:
            return f"Notification: {self.text}"
