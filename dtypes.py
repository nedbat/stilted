"""Data types for stilted."""

from types import UnionType
from dataclasses import dataclass

Number: UnionType = int|float

@dataclass
class Name:
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
