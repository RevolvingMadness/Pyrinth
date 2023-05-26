"""Utility functions for Pyrinth."""
import datetime as _datetime
import json as _json
import typing as _typing

import dateutil.parser as _parser

import pyrinth.projects as _projects


def to_sentence_case(sentence: str) -> _typing.Any:
    return sentence.title().replace("-", " ").replace("_", " ")


def remove_null_values(json: dict) -> dict:
    result = {}
    for key, value in json.items():
        if value is not None:
            result.update({key: value})
    return result


def to_image_from_json(json: dict) -> list:
    return [_projects.Project.GalleryImage._from_json(image) for image in json]


def json_to_query_params(json: dict) -> str:
    result = ""
    for key, value in json.items():
        result += f"{key}={_json.dumps(value)}&"
    return result


def remove_file_path(file) -> str:
    return "".join(file.split("/")[-1])


def list_to_json(lst: list) -> list[dict]:
    result = []
    for item in lst:
        if not isinstance(item, dict):
            result.append(item._to_json())
        else:
            result.append(item)
    return result


def list_to_object(type_, lst) -> list:
    result = []
    for item in lst:
        if isinstance(item, dict):
            result.append(type_._from_json(item))
        else:
            result.append(item)
    return result


def format_time(time) -> _datetime.datetime:
    return _parser.parser().parse(time)


def args_to_dict(**kwargs) -> str:
    return _json.dumps(kwargs)
