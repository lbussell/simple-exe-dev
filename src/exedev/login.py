"""Who's making a request, from the headers exe.dev's proxy adds.

https://exe.dev/docs/login-with-exe.md
"""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Identity:
    user_id: str
    email: str


def get_identity(headers: Mapping[str, str]) -> Identity | None:
    """The signed-in user, or None if the request didn't come through exe.dev login."""
    user_id = headers.get("X-ExeDev-UserID")
    if not user_id:
        return None
    return Identity(user_id, headers.get("X-ExeDev-Email", ""))
