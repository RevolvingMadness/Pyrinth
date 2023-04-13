"""Utility functions for Pyrinth."""

import json
import typing
import datetime
import dateutil.parser
import pyrinth.projects as projects


def to_sentence_case(sentence) -> typing.Any:
    """Utility Function."""
    return sentence.title().replace("-", " ").replace("_", " ")


def remove_null_values(json_: dict) -> dict:
    """Utility Function."""
    result = {}
    for key, value in json_.items():
        if value is not None:
            result.update({key: value})

    return result


def to_image_from_json(json_: dict) -> list:
    """Utility Function."""
    return [projects.Project.GalleryImage.from_json(image) for image in json_]


def json_to_query_params(json_: dict) -> str:
    """Utility Function."""
    result = ""
    for key, value in json_.items():
        result += f"{key}={json.dumps(value)}&"
    return result


def remove_file_path(file) -> str:
    """Utility Function."""
    return "".join(file.split("/")[-1])


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


def list_to_object(type_, lst) -> list:
    """Utility Function."""
    result = []

    for item in lst:
        if isinstance(item, dict):
            result.append(type_.from_json(item))
        else:
            result.append(item)

    return result


def format_time(time) -> datetime.datetime:
    """Utility Function."""
    return dateutil.parser.parser().parse(time)


def args_to_dict(**kwargs) -> str:
    return json.dumps(kwargs)
