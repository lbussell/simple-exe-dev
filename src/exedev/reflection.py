"""Metadata about this VM.

https://exe.dev/docs/integrations-reflection.md
"""

import json
import urllib.request
from dataclasses import dataclass

URL = "https://reflection.int.exe.xyz/"


@dataclass(frozen=True)
class Info:
    name: str
    emoji: str


@dataclass(frozen=True)
class Integration:
    name: str
    type: str
    comment: str
    help: str


def _get(path: str = "") -> dict:
    with urllib.request.urlopen(URL + path) as response:
        return json.load(response)


def get_info() -> Info:
    index = _get()
    return Info(index["name"], index["emoji"])


def get_email() -> str:
    return _get("email")["email"]


def get_tags() -> list[str]:
    return _get("tags")["tags"]


def get_comment() -> str:
    return _get("comment")["comment"]


def get_default_port() -> int:
    return _get("default_port")["default_port"]


def get_integrations() -> list[Integration]:
    return [
        Integration(i["name"], i["type"], i["comment"], i["help"])
        for i in _get("integrations")["integrations"]
    ]
