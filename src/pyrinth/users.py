"""Used for users."""
from __future__ import annotations

import dataclasses
import datetime as _datetime
import json as _json
import typing as _typing

import requests as _requests

import pyrinth.exceptions as _exceptions
import pyrinth.models as _models
import pyrinth.projects as _projects
import pyrinth.util as _util


class User:
    def __init__(self, user_model: _models._UserModel) -> None:
        self.user_model = user_model

    def __repr__(self) -> str:
        return f"User: {(self.user_model.name if self.user_model.name else self.user_model.username)}"

    @property
    def auth(self) -> str:
        return self.user_model.auth

    @staticmethod
    def _from_json(json_: dict) -> User:
        return User(_models._UserModel._from_json(json_))

    @property
    def payout_history(self) -> _PayoutHistory:
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/user/{self.user_model.username}/payouts",
            headers={"authorization": self.user_model.auth},
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to get this user's payout history"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return User._PayoutHistory(
            response["all_time"], response["last_month"], response["payouts"]
        )

    def withdraw_balance(self, amount: int) -> _typing.Literal[True]:
        raw_response = _requests.post(
            f"https://api.modrinth.com/v2/user/{self.user_model.id}/payouts",
            headers={
                "content-type": "application/json",
                "authorization": self.user_model.auth,
            },
            json={"amount": amount},
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to withdraw this user's balance"
                )
            case 404:
                raise _exceptions.NotFoundError("The requested user was not found")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    def change_avatar(self, file_path) -> _typing.Literal[True]:
        raw_response = _requests.patch(
            f"https://api.modrinth.com/v2/user/{self.user_model.id}/icon",
            headers={"authorization": self.user_model.auth},
            params={"ext": file_path.split(".")[-1]},
            data=open(file_path, "rb"),
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.InvalidParamError("Invalid format for new icon")
            case 404:
                raise _exceptions.NotFoundError("The requested user was not found")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    @staticmethod
    def get(id_: str, auth=None) -> User:
        """Get a user.

        Args:
            id_ (str): The user's ID to find
            auth (str, optional): The authorization token to use when creating the user. Defaults to None

        Raises:
            NotFoundError: The user was not found
            InvalidRequestError: An invalid API call was sent

        Returns:
            (User): The user that was found
        """
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/user/{id_}", timeout=60
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError("The requested user was not found")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        response.update({"authorization": auth})
        return User(_models._UserModel._from_json(response))

    @property
    def date_created(self) -> _datetime.datetime:
        return _util.format_time(self.user_model.created)

    @property
    def followed_projects(self) -> list[_projects.Project]:
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/user/{self.user_model.username}/follows",
            headers={"authorization": self.user_model.auth},
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to get this user's followed projects"
                )
            case 404:
                raise _exceptions.NotFoundError("The requested user was not found")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return [
            _projects.Project(_models.ProjectModel._from_json(project_json))
            for project_json in response
        ]

    @property
    def notifications(self) -> list[_Notification]:
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/user/{self.user_model.username}/notifications",
            headers={"authorization": self.user_model.auth},
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to get this user's notifications"
                )
            case 404:
                raise _exceptions.NotFoundError("The requested user was not found")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return [
            User._Notification._from_json(notification) for notification in response
        ]

    def create_project(
        self, project_model: _models.ProjectModel, icon: str | None = None
    ) -> int:
        """
        Create a project.

        Args:
            project_model (ProjectModel): The model of the project to create
            icon (str): The path of the icon to use for the newly created project

        Returns:
            (int): If the project creation was successful
        """
        files: dict = {"data": project_model._to_bytes()}
        if icon:
            files.update({"icon": open(icon, "rb")})
        raw_response = _requests.post(
            "https://api.modrinth.com/v2/project",
            files=files,
            headers={"authorization": self.user_model.auth},
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to create a project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    @property
    def projects(self) -> list[_projects.Project]:
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/user/{self.user_model.id}/projects",
            timeout=60,
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError("The requested user was not found")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return [
            _projects.Project(_models.ProjectModel._from_json(project_json))
            for project_json in response
        ]

    def follow_project(self, id_: str) -> int:
        """
        Follow a project.

        Args:
            id_ (str): The ID of the project to follow

        Returns:
            (int): If the project follow was successful
        """
        raw_response = _requests.post(
            f"https://api.modrinth.com/v2/project/{id_}/follow",
            headers={"authorization": self.user_model.auth},
            timeout=60,
        )
        match raw_response.status_code:
            case 400:
                raise _exceptions.NotFoundError(
                    "The requested project was not found or you are already following the specified project"
                )
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to follow a project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    def unfollow_project(self, id_: str) -> int:
        """
        Unfollow a project.

        Args:
            id_ (str): The ID of the project to unfollow

        Returns:
            (int): If the project unfollow was successful
        """
        raw_response = _requests.delete(
            f"https://api.modrinth.com/v2/project/{id_}/follow",
            headers={"authorization": self.user_model.auth},
            timeout=60,
        )
        match raw_response.status_code:
            case 400:
                raise _exceptions.NotFoundError(
                    "The requested project was not found or you are not following the specified project"
                )
            case 401:
                raise _exceptions.NoAuthorizationError(
                    "No authorization to unfollow a project"
                )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return True

    @staticmethod
    def get_from_auth(auth: str) -> User:
        """
        Get a user from authorization token.

        Returns:
            (User): The user that was found using the authorization token
        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/user",
            headers={"authorization": auth},
            timeout=60,
        )
        match raw_response.status_code:
            case 401:
                raise _exceptions.InvalidParamError("Invalid authorization token")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        response.update({"authorization": auth})
        return User._from_json(response)

    @staticmethod
    def from_id(id_: str) -> User:
        """
        Get a user from ID.

        Returns
            (User): The user that was found using the ID

        """
        raw_response = _requests.get(
            f"https://api.modrinth.com/v2/user/{id_}", timeout=60
        )
        match raw_response.status_code:
            case 404:
                raise _exceptions.NotFoundError("The requested user was not found")
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        return User._from_json(raw_response.json())

    @staticmethod
    def from_ids(ids: list[str]) -> list[User]:
        """
        Get a users from IDs.

        Returns:
            (User): The users that were found using the IDs

        """
        raw_response = _requests.get(
            "https://api.modrinth.com/v2/users",
            params={"ids": _json.dumps(ids)},
            timeout=60,
        )
        if not raw_response.ok:
            raise _exceptions.InvalidRequestError(raw_response.text)
        response: dict = raw_response.json()
        return [User.get(user.get("username")) for user in response]

    class _Notification:
        """Used for the user's notifications."""

        id_: str
        user_id: str
        type: str
        title: str
        text: str
        link: str
        read: str
        created: str
        actions: str
        project_title: str

        def __repr__(self) -> str:
            return f"Notification: {self.text}"

        @staticmethod
        def _from_json(notification_json: dict) -> User._Notification:
            result = User._Notification()
            result.id_ = notification_json.get("id", ...)
            result.user_id = notification_json.get("user_id", ...)
            result.type = notification_json.get("type", ...)
            result.title = notification_json.get("title", ...)
            result.text = notification_json.get("text", ...)
            result.link = notification_json.get("link", ...)
            result.read = notification_json.get("read", ...)
            result.created = notification_json.get("created", ...)
            result.actions = notification_json.get("actions", ...)
            result.project_title = result.title.split("**")[1]
            return result

    @dataclasses.dataclass
    class _PayoutHistory:
        all_time: float
        last_month: float
        payouts: list

        def __repr__(self) -> str:
            return f"PayoutHistory: {self.all_time}"
