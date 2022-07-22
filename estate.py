"""Execution state and helpers for stilted."""

from __future__ import annotations
from collections import ChainMap
from dataclasses import dataclass
from typing import Any

from error import Tilted
from dtypes import Bool, MARK, Name, Procedure

# The `systemdict` dict for all builtin names.
SYSTEMDICT: dict[str, Any] = {
    "false": Bool(literal=True, value=False),
    "true": Bool(literal=True, value=True),
}


@dataclass
class ExecState:
    """The stilted execution state."""

    dstack: ChainMap
    ostack: list[Any]
    estack: list[Any]
    userdict: dict[str, Any]

    @classmethod
    def new(cls) -> ExecState:
        """Start a brand-new execution state."""
        userdict: dict[str, Any] = {}
        return cls(
            dstack=ChainMap(userdict, SYSTEMDICT),
            ostack=[],
            estack=[],
            userdict=userdict,
        )

    def opop(self, n: int) -> list[Any]:
        """Remove the top n operands and return them."""
        self.ohas(n)
        vals = self.ostack[-n:]
        del self.ostack[-n:]
        return vals

    def opush(self, *vals) -> None:
        """Push values on the operand stack."""
        self.ostack.extend(vals)

    def ohas(self, n: int) -> None:
        """Operand stack must have n entries, or stackunderflow."""
        if len(self.ostack) < n:
            raise Tilted("stackunderflow")

    def run_proc(self, proc: Procedure) -> None:
        """Start running a procedure."""
        self.estack.append(iter(proc.objs))

    def run_name(self, name: str) -> None:
        """Run a name."""
        self.estack.append(iter([Name(False, name)]))

    def counttomark(self) -> int:
        """How deep is the nearest mark on the operand stack?"""
        for i, val in enumerate(reversed(self.ostack)):
            if val is MARK:
                return i
        raise Tilted("unmatchedmark")


def operator(arg):
    """
    @operator
    def showpage(...):
        ...

    or:

    @operator("[")
    def mark(...):
        ...

    Returns None: the decorated function is only available through execution,
    not under its Python name.

    """
    if isinstance(arg, str):
        def _dec(func):
            SYSTEMDICT[arg] = func
        return _dec
    else:
        SYSTEMDICT[arg.__name__] = arg
