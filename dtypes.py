"""Data types for stilted."""

from types import UnionType
from typing import Any, Callable, ClassVar
from dataclasses import dataclass

from error import Tilted

@dataclass
class Object:
    """Base class for all Stilted data objects."""
    typename: ClassVar[str] = "object"
    literal: bool

    def op_eq(self) -> str:
        return "--nostringval--"

    def op_eqeq(self) -> str:
        return f"-{self.typename}-"


@dataclass
class Integer(Object):
    """An integer."""
    typename: ClassVar[str] = "integer"
    value: int

    @classmethod
    def from_string(cls, s: str):
        """Convert a string into an Integer."""
        return cls(True, int(s))

    def op_eq(self) -> str:
        return str(self.value)

    def op_eqeq(self) -> str:
        return str(self.value)


@dataclass
class Real(Object):
    """A real (float)."""
    typename: ClassVar[str] = "real"
    value: float

    @classmethod
    def from_string(cls, s):
        """Convert a string into a Real."""
        return cls(True, float(s))

    def op_eq(self) -> str:
        return str(self.value)

    def op_eqeq(self) -> str:
        return str(self.value)


@dataclass
class Boolean(Object):
    """A boolean."""
    typename: ClassVar[str] = "boolean"
    value: bool

    def op_eq(self) -> str:
        return str(self.value).lower()

    def op_eqeq(self) -> str:
        return str(self.value).lower()


@dataclass
class String(Object):
    """A string."""
    typename: ClassVar[str] = "string"
    value: str

    def op_eq(self) -> str:
        return self.value

    def op_eqeq(self) -> str:
        eqeq = "("
        for ch in self.value:
            if ch in "()\\":
                eqeq += "\\" + ch
            elif ch in "\n\t\r":
                eqeq += repr(ch)[1:-1]
            elif "\x00" <= ch < "\x20":
                eqeq += f"\\{ord(ch):03o}"
            else:
                eqeq += ch
        eqeq += ")"
        return eqeq


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

    typename: ClassVar[str] = "name"
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

    def op_eq(self) -> str:
        return self.value

    def op_eqeq(self) -> str:
        return ("/" if self.literal else "") + self.value


class Mark(Object):
    """A mark. There is only one."""
    typename: ClassVar[str] = "mark"


MARK = Mark(literal=False)


@dataclass
class Operator(Object):
    """A built-in operator."""
    typename: ClassVar[str] = "operator"
    value: Callable[[Any], None]


@dataclass
class Procedure(Object):
    """A procedure in curly braces."""

    objs: list[Any]

    def __repr__(self):
        return "<Proc {" + " ".join(map(repr, self.objs)) + "}>"
