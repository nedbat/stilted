"""Execution state and helpers for stilted."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any

from error import Tilted
from dtypes import from_py, Dict, MARK, Name, Object, Operator, Procedure, String

# The `systemdict` dict for all builtin names.
SYSTEMDICT = Dict(literal=True, value={})

SYSTEMDICT["false"] = from_py(False)
SYSTEMDICT["true"] = from_py(True)
SYSTEMDICT["systemdict"] = SYSTEMDICT


@dataclass
class ExecState:
    """The stilted execution state."""

    dstack: list[Dict]
    ostack: list[Object]
    estack: list[Any]
    userdict: Dict
    stdout: Any

    @classmethod
    def new(cls) -> ExecState:
        """Start a brand-new execution state."""
        userdict = Dict(literal=True, value={})
        return cls(
            dstack=[SYSTEMDICT, userdict],
            ostack=[],
            estack=[],
            userdict=userdict,
            stdout=sys.stdout,
        )

    def opop(self) -> Any:
        """Remove the top operand and return it."""
        self.ohas(1)
        return self.ostack.pop()

    def opopn(self, n: int) -> list[Any]:
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

    def dstack_value(self, name: Name | String) -> Object | None:
        """Look in dstack for `name`. If found, return the value."""
        d = self.dstack_dict(name)
        if d is not None:
            return d[name.value]
        return None

    def dstack_dict(self, name: Name | String) -> Dict | None:
        """Look in dstack for `name`. If found, return the Dict."""
        for d in reversed(self.dstack):
            if name.value in d:
                return d
        return None


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
