"""Contains literals for Pyrinth."""
import typing as _typing

index_literal = _typing.Literal[
    "relevance", "downloads", "follows", "newest", "updated"
]
side_literal = _typing.Literal["required", "optional", "unsupported"]
version_status_literal = _typing.Literal[
    "listed", "archived", "draft", "unlisted", "scheduled", "unknown"
]
requested_version_status_literal = _typing.Literal[
    "listed", "archived", "draft", "unlisted"
]
project_status_literal = _typing.Literal[
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
requested_project_status_literal = _typing.Literal[
    "approved", "archived", "unlisted", "private", "draft"
]
version_type_literal = _typing.Literal["release", "beta", "alpha"]
project_type_literal = _typing.Literal["mod", "modpack", "resourcepack", "shader"]
user_role_literal = _typing.Literal["admin", "moderator", "developer"]
sha_algorithm_literal = _typing.Literal["sha512", "sha1"]
