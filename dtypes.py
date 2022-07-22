"""Data types for stilted."""

from types import UnionType
from typing import Any
from dataclasses import dataclass

from error import Tilted

@dataclass
class Obj:
    """Base class for all Stilted data objects."""
    literal: bool

@dataclass
class Int(Obj):
    """An integer."""
    value: int

    @classmethod
    def from_string(cls, s: str):
        """Convert a string into an Int."""
        return cls(True, int(s))


@dataclass
class Float(Obj):
    """A float."""
    value: float

    @classmethod
    def from_string(cls, s):
        """Convert a string into a Float."""
        return cls(True, float(s))


@dataclass
class Bool(Obj):
    """A boolean."""
    value: bool


@dataclass
class String(Obj):
    """A string."""
    value: str


# For type-checking numbers.
Number: UnionType = Int | Float

def from_py(val: Any) -> Obj:
    """Convert any Python value into the appropriate Stilted object."""
    match val:
        case bool():
            return Bool(True, val)
        case str():
            return String(True, val)
        case int():
            return Int(True, val)
        case float():
            return Float(True, val)
        case _:
            raise Exception(f"Buh? from_py({val=})")


def typecheck(a_type, *vals) -> None:
    """Check that all the arguments are the right type."""
    for val in vals:
        if not isinstance(val, a_type):
            raise Tilted("typecheck")


@dataclass
class Name(Obj):
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


class Mark(Obj):
    """A mark. There is only one."""


MARK = Mark(False)


@dataclass
class Procedure(Obj):
    """A procedure in curly braces."""

    objs: list[Any]

    def __repr__(self):
        return "<Proc {" + " ".join(map(repr, self.objs)) + "}>"
