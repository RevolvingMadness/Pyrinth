import pyrinth.users as _users

class _Team:
    members_: dict
    id_: str
    @property
    def members(self) -> list['_Team._TeamMember']: ...
    class _TeamMember:
        team_id: str
        role: str
        permissions: object
        accepted: bool
        payouts_split: object
        ordering: int
        @property
        def user(self) -> _users._User: ...
