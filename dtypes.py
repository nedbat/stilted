"""Data types for stilted."""

from types import UnionType
from typing import Any
from dataclasses import dataclass

from error import Tilted

# For type-checking numbers.
Number: UnionType = int | float

def typecheck(a_type, *vals) -> None:
    """Check that all the arguments are the right type."""
    for val in vals:
        if not isinstance(val, a_type):
            raise Tilted("typecheck")


@dataclass
class Name:
    """A name, either /literal or not."""

    name: str
    literal: bool = False

    def __str__(self):
        return self.name

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
