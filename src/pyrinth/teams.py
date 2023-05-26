import pyrinth.users as _users


class _Team:
    members_: dict
    id_: str

    @property
    def members(self) -> list["_Team._TeamMember"]:
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
        def user(self) -> "_users.User":
            return _users.User._from_json(self._user)

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
