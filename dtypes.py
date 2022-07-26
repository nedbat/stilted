"""Data types for stilted."""

from __future__ import annotations
from types import UnionType
from typing import Any, Callable, ClassVar, Generic, TypeVar
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

# For type-checking numbers.
Number: UnionType = Integer | Real


@dataclass
class Boolean(Object):
    """A boolean."""
    typename: ClassVar[str] = "boolean"
    value: bool

    def op_eq(self) -> str:
        return str(self.value).lower()

    def op_eqeq(self) -> str:
        return str(self.value).lower()

T = TypeVar("T")

@dataclass
class SaveableObject(Object, Generic[T]):
    """A value that can be save/restored."""
    values: list[tuple[Save, T]]

    @property
    def value(self) -> T:
        return self.values[-1][1]

    def prep_for_change(self, save: Save) -> None:
        """Call this before mutating a saveable object."""
        if self.values[-1][0] is not save:
            save.changed_objs.append(self)
            self.values.append((save, self._copy_for_restore()))

    def _copy_for_restore(self) -> T:
        """Make a new copy of the real data, for later restoring."""
        raise NotImplemented


@dataclass
class Save(Object):
    """A VM snapshot object."""
    typename: ClassVar[str] = "save"
    serial: int
    is_valid: bool
    changed_objs: list[SaveableObject]


@dataclass
class String(Object):
    """A string, a mutable array of bytes"""
    typename: ClassVar[str] = "string"
    value: bytearray

    @property
    def str_value(self) -> str:
        return self.value.decode("iso8859-1")

    def op_eq(self) -> str:
        return self.str_value

    def op_eqeq(self) -> str:
        eqeq = "("
        for b in self.value:
            ch = chr(b)
            if ch in "()\\":
                eqeq += "\\" + ch
            elif ch in "\n\t\r":
                eqeq += repr(ch)[1:-1]
            elif "\x00" <= ch < "\x20":
                eqeq += f"\\{b:03o}"
            else:
                eqeq += ch
        eqeq += ")"
        return eqeq


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

    @property
    def str_value(self) -> str:
        return self.value

    def op_eq(self) -> str:
        return self.value

    def op_eqeq(self) -> str:
        return ("/" if self.literal else "") + self.value

Stringy: UnionType = Name | String



class Mark(Object):
    """A mark. There is only one."""
    typename: ClassVar[str] = "mark"

MARK = Mark(literal=True)


class Null(Object):
    """A null. There is only one."""
    typename: ClassVar[str] = "null"

    def op_eqeq(self) -> str:
        return "null"

NULL = Null(literal=True)




@dataclass
class Dict(SaveableObject[dict[str, Object]]):
    """A dictionary."""
    typename: ClassVar[str] = "dict"

    def _copy_for_restore(self) -> dict[str, Object]:
        return dict(self.value)

    def __getitem__(self, name: str) -> Object:
        return self.value[name]

    def __setitem__(self, name: str, value: Object) -> None:
        self.value[name] = value

    def __contains__(self, name: str) -> bool:
        return name in self.value


@dataclass
class Operator(Object):
    """A built-in operator."""
    typename: ClassVar[str] = "operator"
    value: Callable[[Any], None]

    def op_eq(self) -> str:
        return self.value.__name__

    def op_eqeq(self) -> str:
        return "--" + self.value.__name__ + "--"


@dataclass
class Procedure(Object):
    """A procedure in curly braces."""

    objs: list[Object]

    def __repr__(self):
        return "<Proc {" + " ".join(map(repr, self.objs)) + "}>"


def from_py(val: Any) -> Object:
    """Convert a simple Python value into the appropriate Stilted object."""
    match val:
        case bool():
            return Boolean(True, val)
        case float():
            return Real(True, val)
        case int():
            return Integer(True, val)
        case None:
            return NULL
        case str():
            return String(True, bytearray(val.encode("iso8859-1")))
        case _:
            raise Exception(f"Buh? from_py({val=})")


def typecheck(a_type, *vals) -> None:
    """Check that all the arguments are the right type."""
    for val in vals:
        if not isinstance(val, a_type):
            raise Tilted(f"typecheck: expected {a_type}, got {type(val)}")
