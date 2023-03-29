"""Utility functions for Pyrinth."""

import json
from typing import Any
from datetime import datetime
from dateutil.parser import parser


def to_sentence_case(sentence) -> Any:
    """Utility Function."""
    return sentence.title().replace('-', ' ').replace('_', ' ')


def remove_null_values(json_: dict) -> dict:
    """Utility Function."""
    result = {}
    for key, value in json_.items():
        if value is not None:
            result.update({key: value})

    return result


def to_image_from_json(json_: dict) -> list:
    """Utility Function."""
    from pyrinth.projects import Project
    return [Project.GalleryImage.from_json(image) for image in json_]


def json_to_query_params(json_: dict) -> str:
    """Utility Function."""
    result = ''
    for key, value in json_.items():
        result += f'{key}={json.dumps(value)}&'
    return result


def remove_file_path(file) -> str:
    """Utility Function."""
    return ''.join(file.split('/')[-1])


def list_to_json(lst: list) -> list[dict]:
    """Utility Function."""
    result = []

    for item in lst:
        if not isinstance(item, dict):
            # Convert it to json format
            result.append(item.to_json())
        else:
            # It's already in json format
            result.append(item)

    return result


def format_time(time) -> datetime:
    """Utility Function."""
    return parser().parse(time)
