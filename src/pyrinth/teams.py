import pyrinth.users as _users


class _Team:
    """
    Represents a team

    Attributes:
        members (list[dict]): A list of team members
        id (str): The ID of the team

    """

    members_: dict
    id_: str

    @property
    def members(self) -> list["_Team._TeamMember"]:
        """
        Gets a list of team members

        Returns:
            (list[Project.TeamMember]): A list of team members
        """
        return [
            _Team._TeamMember._from_json(team_member) for team_member in self.members_
        ]

    @staticmethod
    def _from_json(team_json: dict) -> "_Team":
        result = _Team()
        result.members_ = team_json
        result.id_ = team_json[0]["team_id"]
        return result

    class _TeamMember:
        """Represents a team member of a project

        Attributes:
            team_id (str): The ID of the team member belongs to
            user (dict): The user associated with the team member
            role (str): The role of the team member within the team
            permissions: The permissions of the team member within the team
            accepted (bool): Whether the team member has accepted their invitation to join the team
            payouts_split: The percentage of payouts that the team member receives
            ordering (int): The ordering of the team member within the team

        """

        team_id: str
        _user: dict
        role: str
        permissions: object
        accepted: bool
        payouts_split: object
        ordering: int

        def __repr__(self) -> str:
            return "Team Member"

        @property
        def user(self) -> "_users._User":
            """Gets the user associated with the team member

            Returns:
                (User): The user associated with the team member
            """
            return _users._User._from_json(self._user)

        @staticmethod
        def _from_json(team_member_json: dict) -> "_Team._TeamMember":
            result = _Team._TeamMember()
            result.team_id = team_member_json.get("team_id", ...)
            result._user = team_member_json.get("user", ...)
            result.role = team_member_json.get("role", ...)
            result.permissions = team_member_json.get("permissions")
            result.accepted = team_member_json.get("accepted", ...)
            result.payouts_split = team_member_json.get("payouts_split")
            result.ordering = team_member_json.get("ordering", ...)
            return result
