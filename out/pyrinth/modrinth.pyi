import pyrinth.projects as projects
from _typeshed import Incomplete

class Modrinth:
    @staticmethod
    def project_exists(id_: str) -> bool: ...
    @staticmethod
    def get_random_projects(count: int = ...) -> list["projects.Project"]: ...

    class Statistics:
        authors: Incomplete
        files: Incomplete
        projects: Incomplete
        versions: Incomplete
        def __init__(self) -> None: ...
