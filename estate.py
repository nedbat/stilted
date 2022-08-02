"""Execution state and helpers for Stilted."""

from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass, field
from typing import Any, Iterator

from error import Tilted
from dtypes import (
    from_py, typecheck,
    Array, ArrayStorage, Dict, DictStorage, MARK, Name, NULL,
    Object, Operator, Save, SaveableObject, String,
)

# The `systemdict` dict for all builtin names.
SYSTEMDICT: dict[str, Object] = {}

SYSTEMDICT["false"] = from_py(False)
SYSTEMDICT["null"] = from_py(None)
SYSTEMDICT["true"] = from_py(True)


@dataclass
class ExecState:
    """The Stilted execution state."""

    # Dictionary stack
    dstack: list[Dict] = field(default_factory=list)

    # Operand stack
    ostack: list[Object] = field(default_factory=list)

    # Execution stack. This is a mix of:
    #   1) Iterators of Stilted Objects (procedures)
    #   2) Python functions (used for internal work)
    #   3) Lists of arguments for functions from #2.
    estack: list[Any] = field(default_factory=list)

    # Save-object stack
    sstack: list[Save] = field(default_factory=list)

    # The stdout file object
    stdout: Any = field(default_factory=lambda: sys.stdout)

    # Sequence of serial numbers for save objects
    save_serials: Iterator[int] = field(default_factory=itertools.count)

    @classmethod
    def new(cls) -> ExecState:
        """Start a brand-new execution state."""
        estate = cls()
        estate.new_save()

        systemdict = estate.new_dict(value=SYSTEMDICT)
        systemdict["systemdict"] = systemdict
        estate.dstack.append(systemdict)

        userdict = estate.new_dict()
        systemdict["userdict"] = userdict
        estate.dstack.append(userdict)

        return estate

    def opop(self, a_type=None) -> Any:
        """
        Remove the top operand and return it.

        Optionally typecheck the value with `a_type`.
        """
        self.ohas(1)
        obj = self.ostack.pop()
        if a_type is not None:
            typecheck(a_type, obj)
        return obj

    def opopn(self, n: int) -> list[Any]:
        """Remove the top n operands and return them."""
        self.ohas(n)
        if n == 0:
            vals = []
        else:
            vals = self.ostack[-n:]
            del self.ostack[-n:]
        return vals

    def opush(self, *vals: Object) -> None:
        """Push values on the operand stack."""
        self.ostack.extend(vals)

    def ohas(self, n: int) -> None:
        """Operand stack must have n entries, or stackunderflow."""
        if len(self.ostack) < n:
            raise Tilted("stackunderflow")

    def run_proc(self, proc: Array) -> None:
        """Start running a procedure."""
        self.estack.append(iter(proc.value))

    def run_name(self, name: str) -> None:
        """Run a name."""
        self.estack.append(iter([Name(False, name)]))

    def counttomark(self) -> int:
        """How deep is the nearest mark on the operand stack?"""
        for i, val in enumerate(reversed(self.ostack)):
            if val is MARK:
                return i
        raise Tilted("unmatchedmark")

    def new_array(self, n: int=None, value: list[Object]=None) -> Array:
        """Make a new Array, either by size or contents."""
        if value is None:
            assert n is not None
            value = [NULL] * n
        else:
            n = len(value)
        return Array(
            literal=True,
            storage=ArrayStorage(values=[(self.sstack[-1], value)]),
            start=0,
            length=n,
        )

    def new_dict(self, value: dict[str, Object]=None) -> Dict:
        """Make a new Dict."""
        value = value if value is not None else {}
        return Dict(
            literal=True,
            storage=DictStorage(values=[(self.sstack[-1], value)]),
        )

    def dstack_value(self, name: Name | String) -> Object | None:
        """Look in dstack for `name`. If found, return the value."""
        d = self.dstack_dict(name)
        if d is not None:
            return d[name.str_value]
        return None

    def dstack_dict(self, name: Name | String) -> Dict | None:
        """Look in dstack for `name`. If found, return the containing Dict."""
        for d in reversed(self.dstack):
            if name.str_value in d:
                return d
        return None

    def prep_for_change(self, d: SaveableObject) -> None:
        """An object is about to change. Do save/restore bookkeeping."""
        d.prep_for_change(self.sstack[-1])

    def new_save(self) -> Save:
        """Make a new save-point."""
        save = Save(
            literal=True,
            serial=next(self.save_serials),
            is_valid=True,
            changed_objs=[],
        )
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
            assert arg not in SYSTEMDICT
            SYSTEMDICT[arg] = Operator(literal=False, value=func, name=arg)
        return _dec
    else:
        name = arg.__name__
        assert name not in SYSTEMDICT
        SYSTEMDICT[name] = Operator(literal=False, value=arg, name=name)
