"""Execution state and helpers for stilted."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any

from error import Tilted
from dtypes import (
    from_py, Dict, MARK, Name, Object, Operator, Procedure, Save,
    SaveableObject, String,
)

# The `systemdict` dict for all builtin names.
SYSTEMDICT: dict[str, Object] = {}

SYSTEMDICT["false"] = from_py(False)
SYSTEMDICT["true"] = from_py(True)


@dataclass
class ExecState:
    """The stilted execution state."""

    dstack: list[Dict]
    ostack: list[Object]
    estack: list[Any]
    sstack: list[Save]
    stdout: Any

    @classmethod
    def new(cls) -> ExecState:
        """Start a brand-new execution state."""
        estate = cls(
            dstack=[],
            ostack=[],
            estack=[],
            sstack=[],
            stdout=sys.stdout,
        )

        estate.new_save()

        systemdict = estate.new_dict(value=SYSTEMDICT)
        systemdict["systemdict"] = systemdict
        estate.dstack.append(systemdict)

        userdict = estate.new_dict()
        systemdict["userdict"] = userdict
        estate.dstack.append(userdict)

        return estate

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

    def new_dict(self, value: dict[str, Object]=None) -> Dict:
        """Make a new Dict."""
        value = value if value is not None else {}
        return Dict(
            literal=True,
            values=[(self.sstack[-1], value)],
        )

    def dstack_dict(self, name: Name | String) -> Dict | None:
        """Look in dstack for `name`. If found, return the Dict."""
        for d in reversed(self.dstack):
            if name.value in d:
                return d
        return None

    def prep_for_change(self, d: SaveableObject) -> None:
        """An object is about to change. Do save/restore bookkeeping."""
        d.prep_for_change(self.sstack[-1])

    def new_save(self) -> Save:
        """Make a new save-point."""
        save = Save(literal=True, is_valid=True, changed_objs=[])
        self.sstack.append(save)
        return save


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
