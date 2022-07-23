"""Execution state and helpers for stilted."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, ChainMap

from error import Tilted
from dtypes import Boolean, Dict, MARK, Name, Object, Operator, Procedure

# The `systemdict` dict for all builtin names.
SYSTEMDICT: dict[str, Object] = {
    "false": Boolean(literal=True, value=False),
    "true": Boolean(literal=True, value=True),
}

SYSTEMDICT["systemdict"] = Dict(literal=True, value=SYSTEMDICT)


@dataclass
class ExecState:
    """The stilted execution state."""

    dstack: ChainMap[str, Object]
    ostack: list[Object]
    estack: list[Any]
    userdict: dict[str, Any]
    stdout: Any

    @classmethod
    def new(cls) -> ExecState:
        """Start a brand-new execution state."""
        userdict: dict[str, Object] = {}
        return cls(
            dstack=ChainMap(userdict, SYSTEMDICT),
            ostack=[],
            estack=[],
            userdict=userdict,
            stdout=sys.stdout,
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
            assert func.__name__.endswith("_")
            SYSTEMDICT[arg] = Operator(literal=False, value=func)
        return _dec
    else:
        SYSTEMDICT[arg.__name__] = Operator(literal=False, value=arg)
