import json
import requests as r
import pyrinth.users as users


class Team:
    """
    Represents a team.

    Attributes:
        members (list[dict]): A list of team members.
        id (str): The ID of the team.

    Methods:
        get_members: Gets a list of team members.
        _from_json: Creates a Team object from a JSON dictionary.
        get: Gets a team by its ID.
        get_multiple: Gets multiple teams by their IDs.

    """

    def __init__(self):
        """
        Initializes a Team object.
        """
        self.members = None
        self.id = None

    def get_members(self) -> list["Team.TeamMember"]:
        """
        Gets a list of team members.

        Returns:
            (list[Project.TeamMember]): A list of team members.
        """
        return [
            Team.TeamMember._from_json(team_member)
            for team_member in self.members
        ]

    @staticmethod
    def _from_json(list_: dict) -> "Team":
        result = Team()
        result.members = list_
        result.id = list_[0]["team_id"]
        return result

    class TeamMember:
        """Represents a team member of a project.

        Attributes:
            team_id (str): The ID of the team the member belongs to.
            user (dict): The user associated with the team member.
            role (str): The role of the team member within the team.
            permissions: The permissions of the team member within the team.
            accepted (bool): Whether the team member has accepted their invitation to join the team.
            payouts_split: The percentage of payouts that the team member receives.
            ordering (int): The ordering of the team member within the team.

        """

        def __init__(
            self,
            team_id: str,
            user: dict,
            role: str,
            permissions,
            accepted: bool,
            payouts_split,
            ordering: bool
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
            """Gets the user associated with the team member.

            Returns:
                (User): The user associated with the team member.
            """
            return users.User._from_json(self.user)

        @staticmethod
        def _from_json(json_: dict):
            return Team.TeamMember(
                json_.get("team_id"), # type: ignore
                json_.get("user"), # type: ignore
                json_.get("role"), # type: ignore
                json_.get("permissions"),
                json_.get("accepted"), # type: ignore
                json_.get("payouts_split"),
                json_.get("ordering"), # type: ignore
            )
