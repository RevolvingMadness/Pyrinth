import pyrinth.users as users
from _typeshed import Incomplete

class Team:
    members: Incomplete
    id: Incomplete
    def __init__(self) -> None: ...
    def get_members(self) -> list['Team.TeamMember']: ...
    class TeamMember:
        team_id: Incomplete
        user: Incomplete
        role: Incomplete
        permissions: Incomplete
        accepted: Incomplete
        payouts_split: Incomplete
        ordering: Incomplete
        def __init__(self, team_id: str, user: dict, role: str, permissions, accepted: bool, payouts_split, ordering: bool) -> None: ...
        def get_user(self) -> users.User: ...
