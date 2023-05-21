import pyrinth.users as users
from _typeshed import Incomplete

class Team:
    id: Incomplete
    def __init__(self) -> None: ...
    @property
    def members(self) -> list["Team.TeamMember"]: ...

    class TeamMember:
        team_id: Incomplete
        role: Incomplete
        permissions: Incomplete
        accepted: Incomplete
        payouts_split: Incomplete
        ordering: Incomplete
        def __init__(
            self,
            team_id: str,
            user: dict,
            role: str,
            permissions,
            accepted: bool,
            payouts_split,
            ordering: bool,
        ) -> None: ...
        @property
        def user(self) -> users.User: ...
