"""PostScript-specific types."""

from types import UnionType
from dataclasses import dataclass

number: UnionType = int|float

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
    """A mark."""

MARK = Mark()
