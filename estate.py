"""Execution state and helpers for stilted."""

from __future__ import annotations
from collections import ChainMap
from dataclasses import dataclass
from typing import Any

from error import Tilted
from dtypes import MARK

# The `systemdict` dict for all builtin names.
SYSTEMDICT: dict[str, Any] = {}


@dataclass
class ExecState:
    """The stilted execution state."""
    dstack: ChainMap
    ostack: list[Any]
    userdict: dict[str, Any]

    @classmethod
    def new(cls) -> ExecState:
        """Start a brand-new execution state."""
        userdict: dict[str, Any] = {}
        return cls(
            dstack=ChainMap(userdict, SYSTEMDICT),
            ostack=[],
            userdict=userdict,
        )

    def opop(self, n) -> list[Any]:
        """Remove the top n operands and return them."""
        self.ohas(n)
        vals = self.ostack[-n:]
        del self.ostack[-n:]
        return vals

    def opush(self, val) -> None:
        """Push a value on the operand stack."""
        self.ostack.append(val)

    def ohas(self, n) -> None:
        """Operand stack must have n entries, or stackunderflow."""
        if len(self.ostack) < n:
            raise Tilted("stackunderflow")

    def counttomark(self) -> int:
        for i, val in enumerate(reversed(self.ostack)):
            if val is MARK:
                return i
        raise Tilted("unmatchedmark")

def builtin(func):
    """Define a function as a builtin name."""
    SYSTEMDICT[func.__name__] = func
    return func


def builtin_with_name(name: str):
    """Define a builtin function, with a different name."""
    def _dec(func):
        SYSTEMDICT[name] = func
        return func

    return _dec
