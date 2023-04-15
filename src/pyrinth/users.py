"""Used for users."""

import datetime
import json
import typing

import requests as r

import pyrinth.exceptions as exceptions
import pyrinth.models as models
import pyrinth.projects as projects
import pyrinth.util as util


class User:
    """Contains information about users."""

    def __init__(self, user_model: "models.UserModel") -> None:
        self.model = user_model
        if isinstance(user_model, dict):
            self.model = models.UserModel._from_json(user_model)

    def __repr__(self) -> str:
        return f"User: {util.args_to_dict(username=self.model.username, name=self.model.name, id=self.model.id)}"

    def get_auth(self) -> typing.Optional[str]:
        """Gets the users authorization token."""
        return self.model.auth

    @staticmethod
    def _from_json(json_: dict) -> "User":
        """Utility Function."""
        return User(models.UserModel._from_json(json_))

    def get_payout_history(self) -> "User.PayoutHistory":
        raw_response = r.get(
            f"https://api.modrinth.com/v2/user/{self.model.username}/payouts",
            headers={"authorization": self.model.auth},  # type: ignore
            timeout=60
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to get this user's followed projects"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = json.loads(raw_response.content)

        return User.PayoutHistory(response["all_time"], response["last_month"], response["payouts"])

    def withdraw_balance(self, amount: int) -> bool:
        raw_response = r.post(
            f"https://api.modrinth.com/v2/user/{self.model.id}/payouts",
            headers={
                "content-type": "application/json",
                "authorization": self.model.auth  # type: ignore
            },
            json={"amount": amount},
            timeout=60
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to withdraw this user's balance"
            )

        elif raw_response.status_code == 404:
            raise exceptions.NotFoundError("The requested user was not found")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def change_avatar(self, file_path) -> bool:
        raw_response = r.patch(
            f"https://api.modrinth.com/v2/user/{self.model.id}/icon",
            headers={"authorization": self.model.auth},  # type: ignore
            params={"ext": file_path.split('.')[-1]},
            data=open(file_path, "rb"),
            timeout=60
        )

        if raw_response.status_code == 401:
            raise exceptions.InvalidParamError("Invalid format for new icon")

        elif raw_response.status_code == 404:
            raise exceptions.NotFoundError("The requested user was not found")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    @staticmethod
    def get(id_: str, auth=None) -> "User":
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
            f"https://api.modrinth.com/v2/user/{id_}", timeout=60)

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError("The requested user was not found")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = raw_response.json()
        response.update({"authorization": auth})
        return User(response)

    def get_date_created(self) -> datetime.datetime:
        """
        Gets the date of when the user was created.

        Returns:
            datetime: The time of when the user was created
        """
        return util.format_time(self.model.created)

    def get_followed_projects(self) -> list["projects.Project"]:
        """
        Gets a users followed projects.

        Returns:
            list[Project]: The users followed projects
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/user/{self.model.username}/follows",
            headers={"authorization": self.model.auth},  # type: ignore
            timeout=60,
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to get this user's followed projects"
            )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError("The requested user was not found")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        followed_projects = []
        projects_ = json.loads(raw_response.content)
        for project in projects_:
            followed_projects.append(projects_.Project(project))

        return followed_projects

    def get_notifications(self) -> list["User.Notification"]:
        """
        Gets a users notifications.

        Returns:
            list[User.Notification]: The users notifications
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/user/{self.model.username}/notifications",
            headers={"authorization": self.model.auth},  # type: ignore
            timeout=60,
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to get this user's notifications"
            )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError("The requested user was not found")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = json.loads(raw_response.content)
        return [User.Notification(notification) for notification in response]

    def get_amount_of_projects(self) -> int:
        """
        Gets the amount of projects a user has.

        Returns:
            list[Project]: The users projects
        """
        projects_ = self.get_projects()

        return len(projects_)

    def create_project(self, project_model, icon: typing.Optional[str] = None) -> int:
        """
        Creates a project.

        Args:
            project_model (ProjectModel): The model of the project to create.
            icon (str): The path of the icon to use for the newly created project.

        Returns:
            int: If the project creation was successful
        """
        files = {"data": project_model.to_bytes()}
        if icon:
            files.update({"icon": open(icon, "rb")})

        raw_response = r.post(
            "https://api.modrinth.com/v2/project",
            files=files,
            headers={"authorization": self.model.auth},  # type: ignore
            timeout=60,
        )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to create a project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def get_projects(self) -> list["projects.Project"]:
        """
        Gets a users projects.

        Returns:
            list[Project]: The users projects
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/user/{self.model.id}/projects", timeout=60
        )

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError("The requested user was not found")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = json.loads(raw_response.content)
        return [projects.Project(project) for project in response]

    def follow_project(self, id_: str) -> int:
        """
        Follow a project.

        Args:
            id_ (str): The ID of the project to follow

        Returns:
            int: If the project follow was successful
        """
        raw_response = r.post(
            f"https://api.modrinth.com/v2/project/{id_}/follow",
            headers={"authorization": self.model.auth},  # type: ignore
            timeout=60,
        )

        if raw_response.status_code == 400:
            raise exceptions.NotFoundError(
                "The requested project was not found or you are already following the specified project"
            )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to follow a project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    def unfollow_project(self, id_: str) -> int:
        """
        Unfollow a project.

        Args:
            id_ (str): The ID of the project to unfollow

        Returns:
            int: If the project unfollow was successful
        """
        raw_response = r.delete(
            f"https://api.modrinth.com/v2/project/{id_}/follow",
            headers={"authorization": self.model.auth},  # type: ignore
            timeout=60,
        )

        if raw_response.status_code == 400:
            raise exceptions.NotFoundError(
                "The requested project was not found or you are not following the specified project"
            )

        if raw_response.status_code == 401:
            raise exceptions.NoAuthorizationError(
                "No authorization to unfollow a project"
            )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return True

    @staticmethod
    def get_from_auth(auth: str) -> "User":
        """
        Gets a user from authorization token.

        Returns:
            User: The user that was found using the authorization token
        """
        raw_response = r.get(
            "https://api.modrinth.com/v2/user",
            headers={"authorization": auth},
            timeout=60,
        )

        if raw_response.status_code == 401:
            raise exceptions.InvalidParamError("Invalid authorization token")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = raw_response.json()
        response.update({"authorization": auth})
        return User._from_json(response)

    @staticmethod
    def from_id(id_: str) -> "User":
        """
        Gets a user from ID.

        Returns:
            User: The user that was found using the ID
        """
        raw_response = r.get(
            f"https://api.modrinth.com/v2/user/{id_}", timeout=60)

        if raw_response.status_code == 404:
            raise exceptions.NotFoundError("The requested user was not found")

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        return User._from_json(raw_response.json())

    @staticmethod
    def from_ids(ids: list[str]) -> list["User"]:
        """
        Gets a users from IDs.

        Returns:
            User: The users that were found using the IDs
        """
        raw_response = r.get(
            "https://api.modrinth.com/v2/users",
            params={"ids": json.dumps(ids)},
            timeout=60,
        )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError(raw_response.text)

        response = json.loads(raw_response.content)
        return [User.get(user.get("username")) for user in response]

    class Notification:
        """Used for the users notifications."""

        def __init__(self, notification_json: dict) -> None:
            self.id = notification_json.get("id")
            self.user_id = notification_json.get("user_id")
            self.type = notification_json.get("type")
            self.title = notification_json.get("title")
            self.text = notification_json.get("text")
            self.link = notification_json.get("link")
            self.read = notification_json.get("read")
            self.created = notification_json.get("created")
            self.actions = notification_json.get("actions")
            self.project_title = self.title.split("**")[1]  # type: ignore

        def __repr__(self) -> str:
            return f"Notification: {self.text}"

    class PayoutHistory:
        def __init__(self, all_time: float, last_month: float, payouts: list) -> None:
            self.all_time = all_time
            self.last_month = last_month
            self.payouts = payouts
