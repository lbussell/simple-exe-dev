"""Metadata about this VM.

https://exe.dev/docs/integrations-reflection.md
"""

import json
import urllib.request

URL = "https://reflection.int.exe.xyz/"


def _get(path: str = "") -> dict:
    with urllib.request.urlopen(URL + path) as response:
        return json.load(response)


def name() -> str:
    return _get()["name"]


def emoji() -> str:
    return _get()["emoji"]


def email() -> str:
    return _get("email")["email"]


def tags() -> list[str]:
    return _get("tags")["tags"]


def comment() -> str:
    return _get("comment")["comment"]


def default_port() -> int:
    return _get("default_port")["default_port"]


def integrations() -> list[dict]:
    return _get("integrations")["integrations"]
