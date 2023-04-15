"""Utility functions for Pyrinth."""

import datetime
import json
import typing

import dateutil.parser

import pyrinth.projects as projects


def to_sentence_case(sentence) -> typing.Any:
    return sentence.title().replace("-", " ").replace("_", " ")


def remove_null_values(json_: dict) -> dict:
    result = {}
    for key, value in json_.items():
        if value is not None:
            result.update({key: value})

    return result


def to_image_from_json(json_: dict) -> list:
    return [projects.Project.GalleryImage._from_json(image) for image in json_]


def json_to_query_params(json_: dict) -> str:
    result = ""
    for key, value in json_.items():
        result += f"{key}={json.dumps(value)}&"
    return result


def remove_file_path(file) -> str:
    return "".join(file.split("/")[-1])


def list_to_json(lst: list) -> list[dict]:
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
    result = []

    for item in lst:
        if isinstance(item, dict):
            result.append(type_.from_json(item))
        else:
            result.append(item)

    return result


def format_time(time) -> datetime.datetime:
    return dateutil.parser.parser().parse(time)


def args_to_dict(**kwargs) -> str:
    return json.dumps(kwargs)
