"""Contains literals for Pyrinth."""
import typing

index_literal = typing.Literal["relevance", "downloads", "follows", "newest", "updated"]
side_literal = typing.Literal["required", "optional", "unsupported"]
version_status_literal = typing.Literal[
    "listed", "archived", "draft", "unlisted", "scheduled", "unknown"
]
requested_version_status_literal = typing.Literal[
    "listed", "archived", "draft", "unlisted"
]
project_status_literal = typing.Literal[
    "approved",
    "archived",
    "rejected",
    "draft",
    "unlisted",
    "processing",
    "withheld",
    "scheduled",
    "private",
    "unknown",
]
requested_project_status_literal = typing.Literal[
    "approved", "archived", "unlisted", "private", "draft"
]
version_type_literal = typing.Literal["release", "beta", "alpha"]
project_type_literal = typing.Literal["mod", "modpack", "resourcepack", "shader"]
user_role_literal = typing.Literal["admin", "moderator", "developer"]
sha_algorithm_literal = typing.Literal["sha512", "sha1"]
