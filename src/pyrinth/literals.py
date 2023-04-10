from typing import Literal


index_literal = Literal[
    'relevance', 'downloads',
    'follows', 'newest',
    'updated'
]

side_literal = Literal['required', 'optional', 'unsupported']

version_status_literal = Literal[
    'listed', 'archived', 'draft',
    'unlisted', 'scheduled', 'unknown'
]

requested_version_status_literal = Literal[
    'listed', 'archived', 'draft',
    'unlisted'
]

project_status_literal = Literal[
    'approved', 'archived', 'rejected',
    'draft', 'unlisted', 'processing',
    'withheld', 'scheduled', 'private',
    'unknown'
]

requested_project_status_literal = Literal[
    'approved', 'archived', 'unlisted',
    'private', 'draft'
]

version_type_literal = Literal['release', 'beta', 'alpha']

project_type_literal = Literal[
    'mod', 'modpack', 'resourcepack',
    'shader'
]

user_role_literal = Literal['admin', 'moderator', 'developer']
