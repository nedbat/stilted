"""Data types for Stilted."""

from __future__ import annotations

import copy
import math
from types import UnionType
from typing import (
    Any, Callable, ClassVar, Generic, Iterator, TypeVar, TYPE_CHECKING,
)
from dataclasses import dataclass

from error import Tilted
if TYPE_CHECKING:   # pragma: no cover
    from evaluate import Engine

@dataclass
class Object:
    """Base class for all Stilted data objects."""
    # All classes have a typename
    typename: ClassVar[str] = "object"
    # All objects can be literal (True) or executable (False)
    literal: bool

    def op_eq(self) -> str:
        """Produce a string for the `=` operator."""
        return "--nostringval--"

    def op_eqeq(self) -> str:
        """Produce a string for the `==` operator."""
        return f"-{self.typename}-"


@dataclass
class Integer(Object):
    """An integer."""
    typename: ClassVar[str] = "integer"
    value: int

    @classmethod
    def from_string(cls, s: str) -> Integer:
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
    def from_string(cls, s) -> Real:
        """Convert a string into a Real."""
        return cls(True, float(s))

    def __eq__(self, other) -> bool:
        """To make writing tests easier."""
        return math.isclose(self.value, other.value)

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
class SaveableStorage(Generic[T]):
    """
    The storage for saveable objects.

    `values` is a stack of tuples: each has a Save object and a data object.
    When a modification is made to the data, a new tuple is pushed onto the
    stack if the top value isn't already for the current Save object.  Each
    tuple is the copy of the data to restore to for that Save object.

    The `values` stack associates copies of data with the save object they
    correspond to.  This lets the restore operator pop values until the correct
    old copy is found.

    """
    values: list[tuple[Save, T]]

    def prep_for_change(self, save: Save) -> None:
        """Call this before mutating a saveable object."""
        # This implements the "copy on write" for restorable objects.
        if self.values[-1][0] is not save:
            save.changed_objs.append(self)
            self.values.append((save, copy.copy(self.values[-1][1])))


@dataclass
class SaveableObject(Object, Generic[T]):
    """
    An object that can be saved and restored.

    The actual data is in the SaveableStorage object referenced by `storage`.
    """
    storage: SaveableStorage[T]

    @property
    def value(self) -> T:
        """
        The current value of the object's data.

        It's the data from the top SaveableStorage tuple on the stack.
        """
        return self.storage.values[-1][1]

    def prep_for_change(self, save: Save) -> None:
        """Call this before mutating a saveable object."""
        self.storage.prep_for_change(save)


@dataclass
class Save(Object):
    """A VM snapshot object."""
    typename: ClassVar[str] = "save"
    # Each Save object has a serial number so that stale objects on the operand
    # and dictionary stack can be identified.
    serial: int

    # When a Save object is restored, it is marked as invalid to prevent it
    # from being restored twice.
    is_valid: bool

    # All saveable objects that are mutated are pushed onto a list for the
    # current save object.  The restore operator uses the list to find the
    # objects that need to be restored to their old state.
    changed_objs: list[SaveableStorage]


@dataclass
class String(Object):
    """
    A string, a mutable array of bytes.

    Substrings share data with their original string, so all strings have a
    `start` and `length` to go with their bytearray `data`.  When a substring
    is made, it uses the same bytearray as the original, but with new `start`
    and `length`.

    """
    typename: ClassVar[str] = "string"
    data: bytearray
    start: int
    length: int

    @classmethod
    def from_bytes(cls, data: bytes) -> String:
        """Make a new string from a bytestring."""
        return cls(
            literal=True,
            data=bytearray(data),
            start=0,
            length=len(data),
        )

    @classmethod
    def from_size(cls, n: int) -> String:
        """Make a new string with `n` zero bytes."""
        return cls(literal=True, data=bytearray(n), start=0, length=n)

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Iterator[int]:
        for i in range(self.start, self.start + self.length):
            yield self.data[i]

    def __getitem__(self, index: int) -> int:
        return self.data[self.start + index]

    def __setitem__(self, index: int, value: int) -> None:
        self.data[self.start + index] = value

    def new_sub(self, start: int, length: int) -> String:
        """Make a new string as a substring of another."""
        rangecheck(0, start, self.length)
        rangecheck(0, length)
        rangecheck(start + length, self.length)
        return String(
            literal=True,
            data=self.data,
            start=self.start + start,
            length=length,
        )

    @property
    def value(self) -> bytearray:
        """Get the bytearray value of the string."""
        return self.data[self.start: self.start + self.length]

    @property
    def str_value(self) -> str:
        """Get the string value as a Unicode string."""
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

    def __repr__(self):
        return "<Name " + ("/" if self.literal else "") + self.value + ">"

    @classmethod
    def from_string(cls, text: str) -> Name:
        """Make a Name from a string, including leading slash maybe."""
        if text.startswith("/"):
            return cls(True, text[1:])
        else:
            return cls(False, text)

    @property
    def str_value(self) -> str:
        """Get the name as a string."""
        return self.value

    def op_eq(self) -> str:
        return self.value

    def op_eqeq(self) -> str:
        return ("/" if self.literal else "") + self.value

# Many operations are valid on either Names or Strings.
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
class ArrayStorage(SaveableStorage[list[Object]]):
    """Saveable storage for Arrays."""


@dataclass
class Array(SaveableObject[list[Object]]):
    """
    An array.

    Arrays can be subsetted, and the child shares storage with the parent. So
    all Arrays have `start` and `length`.  A new sub-array uses the same
    ArrayStorage, but with new `start` and `length`.

    """
    typename: ClassVar[str] = "array"
    start: int
    length: int

    def new_sub(self, start: int, length: int) -> Array:
        """Make a new array as a substring of another."""
        rangecheck(0, start, self.length)
        rangecheck(0, length)
        rangecheck(start + length, self.length)
        return Array(
            literal=True,
            storage=self.storage,
            start=self.start + start,
            length=length,
        )

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Iterator[Object]:
        for i in range(self.start, self.start + self.length):
            yield self.value[i]

    def __getitem__(self, index: int) -> Object:
        return self.value[self.start + index]

    def __setitem__(self, index: int, value: Object) -> None:
        self.value[self.start + index] = value

    def op_eqeq(self) -> str:
        eqeq = "[" if self.literal else "{"
        eqeq += " ".join(obj.op_eqeq() for obj in self.value)
        eqeq += "]" if self.literal else "}"
        return eqeq


@dataclass
class DictStorage(SaveableStorage[dict[str, Object]]):
    """Saveable storage for Dict objects."""


@dataclass
class Dict(SaveableObject[dict[str, Object]]):
    """A dictionary."""
    typename: ClassVar[str] = "dict"

    def __getitem__(self, name: str) -> Object:
        return self.value[name]

    def __setitem__(self, name: str, value: Object) -> None:
        self.value[name] = value

    def __contains__(self, name: str) -> bool:
        return name in self.value


@dataclass
class Operator(Object):
    """
    A built-in operator.

    `value` is a Python function implementing the operator. `name` is the name
    of the operator, which can differ than the name of the Python function.

    """
    typename: ClassVar[str] = "operator"
    value: Callable[["Engine"], None]
    name: str

    def op_eq(self) -> str:
        return self.name

    def op_eqeq(self) -> str:
        return f"--{self.name}--"


def from_py(val: Any) -> Object:
    """Convert a simple Python value into the appropriate Stilted object."""
    match val:
        case bool(b):
            return Boolean(True, b)
        case float(f):
            return Real(True, f)
        case int(i):
            return Integer(True, i)
        case None:
            return NULL
        case str(s):
            return String.from_bytes(s.encode("iso8859-1"))
        case _:
            raise Exception(f"Buh? from_py({val=})")


def typecheck(a_type, *vals) -> None:
    """Check that all the arguments are the right type."""
    for val in vals:
        if not isinstance(val, a_type):
            if a_type is Number:
                typename = "number"
            elif a_type is Stringy:
                typename = "name"
            else:
                typename = a_type.typename
            raise Tilted("typecheck", f"expected {typename}, got {type(val).typename}")


def rangecheck(lo: int, val: int, hi: int | None=None) -> None:
    """Check that `lo <= val` and `val <= hi`."""
    if not (lo <= val):
        raise Tilted("rangecheck", f"need {lo} <= {val}")
    if hi is not None:
        if not (val <= hi):
            raise Tilted("rangecheck", f"need {val} <= {hi}")
