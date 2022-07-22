"""Data types for stilted."""

from types import UnionType
from typing import Any
from dataclasses import dataclass

from error import Tilted

@dataclass
class Object:
    """Base class for all Stilted data objects."""
    literal: bool

@dataclass
class Integer(Object):
    """An integer."""
    value: int

    @classmethod
    def from_string(cls, s: str):
        """Convert a string into an Integer."""
        return cls(True, int(s))


@dataclass
class Real(Object):
    """A real (float)."""
    value: float

    @classmethod
    def from_string(cls, s):
        """Convert a string into a Real."""
        return cls(True, float(s))


@dataclass
class Boolean(Object):
    """A boolean."""
    value: bool


@dataclass
class String(Object):
    """A string."""
    value: str


# For type-checking numbers.
Number: UnionType = Integer | Real

def from_py(val: Any) -> Object:
    """Convert any Python value into the appropriate Stilted object."""
    match val:
        case bool():
            return Boolean(True, val)
        case str():
            return String(True, val)
        case int():
            return Integer(True, val)
        case float():
            return Real(True, val)
        case _:
            raise Exception(f"Buh? from_py({val=})")


def typecheck(a_type, *vals) -> None:
    """Check that all the arguments are the right type."""
    for val in vals:
        if not isinstance(val, a_type):
            raise Tilted("typecheck")


@dataclass
class Name(Object):
    """A name, either /literal or not."""

    value: str

    def __str__(self):
        return self.value

    def __repr__(self):
        return "<Name " + ("/" if self.literal else "") + self.value + ">"

    @classmethod
    def from_string(cls, text):
        if text.startswith("/"):
            return cls(True, text[1:])
        else:
            return cls(False, text)


class Mark(Object):
    """A mark. There is only one."""


MARK = Mark(False)


@dataclass
class Procedure(Object):
    """A procedure in curly braces."""

    objs: list[Any]

    def __repr__(self):
        return "<Proc {" + " ".join(map(repr, self.objs)) + "}>"
