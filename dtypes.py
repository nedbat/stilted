"""Data types for stilted."""

from types import UnionType
from typing import Any
from dataclasses import dataclass

# For type-checking numbers.
Number: UnionType = int | float


@dataclass
class Name:
    """A name, either /literal or not."""

    name: str
    literal: bool = False

    @classmethod
    def from_string(cls, text):
        if text.startswith("/"):
            return cls(text[1:], literal=True)
        else:
            return cls(text, literal=False)


class Mark:
    """A mark. There is only one."""


MARK = Mark()


@dataclass
class Procedure:
    """A procedure in curly braces."""

    objs: list[Any]
