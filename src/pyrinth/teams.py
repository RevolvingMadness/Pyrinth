import json
import requests as r
import pyrinth.projects as projects
import pyrinth.exceptions as exceptions


class Team:
    def __init__(self):
        self.members = None
        self.id = None

    def get_members(self):
        return [projects.Project.TeamMember.from_json(team_member) for team_member in self.members]

    @staticmethod
    def from_json(list_: dict):
        result = Team()
        result.members = list_
        result.id = list_[0]["team_id"]
        return result

    @staticmethod
    def get(id_: str):
        raw_response = r.get(
            f"https://api.modrinth.com/v2/team/{id_}/members",
            timeout=60
        )

        if not raw_response.ok:
            raise exceptions.InvalidRequestError()

        response = json.loads(raw_response.content)

        return Team.from_json(response)

    @staticmethod
    def get_multiple(ids: list[str]):
        raw_response = r.get(
            f"https://api.modrinth.com/v2/teams",
            params={"ids": json.dumps(ids)},
            timeout=60
        )

        if not raw_response.ok:
            print(raw_response.url)
            raise exceptions.InvalidRequestError()

        response = json.loads(raw_response.content)

        return [Team.from_json(team) for team in response]

    def __repr__(self):
        return f"Team: {len(self.members)} member(s)"
