"""Stack evaluation for stilted."""

from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator

from error import Tilted
from lex import lexer
from dtypes import (
    from_py, typecheck,
    Array, ArrayStorage, Dict, DictStorage, MARK, Name, NULL,
    Object, Operator, Save, SaveableObject, String,
)
from gstate import Device, GstateExtras

# The `systemdict` dict for all builtin names.
SYSTEMDICT: dict[str, Object] = {}

SYSTEMDICT["false"] = from_py(False)
SYSTEMDICT["null"] = from_py(None)
SYSTEMDICT["true"] = from_py(True)


@dataclass
class Engine:
    """Stilted execution engine."""

    # Dictionary stack
    dstack: list[Dict] = field(default_factory=list)

    # Operand stack
    ostack: list[Object] = field(default_factory=list)

    # Execution stack. This is a mix of:
    #   1) Iterators of Stilted Objects (procedures)
    #   2) Python callables (used for internal work)
    estack: list[Any] = field(default_factory=list)

    # Save-object stack
    sstack: list[Save] = field(default_factory=list)

    # gsave stack
    # Most of the graphics state is in PyCairo, but we need other information
    # for each gstate.
    gsaves: list[GstateExtras] = field(default_factory=list)

    # The stdout file object
    stdout: Any = field(default_factory=lambda: sys.stdout)

    # Sequence of serial numbers for save objects
    save_serials: Iterator[int] = field(default_factory=itertools.count)

    # Output device
    device: Device = field(default_factory=Device)

    def __post_init__(self, stdout=None) -> None:
        self.new_save()

        systemdict = self.new_dict(value=SYSTEMDICT)
        systemdict["systemdict"] = systemdict
        self.dstack.append(systemdict)

        userdict = self.new_dict()
        systemdict["userdict"] = userdict
        self.dstack.append(userdict)

        if stdout is not None:
            self.stdout = stdout

    def add_text(self, text: str) -> None:
        """Consume text as Stilted tokens, and add for execution."""
        self.estack.append(self._collect_objects(lexer.tokens(text)))

    def run_text(self, text: str) -> None:
        """Run Stilted text."""
        self.add_text(text)
        self.run()

    def push_string(self, text: str) -> None:
        """Create a String from `text`, and push it on the operand stack."""
        self.opush(String.from_bytes(text.encode("iso8859-1")))

    def _collect_objects(self, tokens: Iterable[Any]) -> Iterator[Any]:
        """Assemble tokens into objects."""
        pstack: list[Any] = []
        for obj in tokens:
            match obj:
                case Name(False, "{"):
                    pstack.append([])

                case Name(False, "}"):
                    if not pstack:
                        raise Tilted("syntaxerror")
                    proc = self.new_array(value=pstack.pop())
                    proc.literal = False
                    if pstack:
                        pstack[-1].append(proc)
                    else:
                        yield proc

                case _:
                    if pstack:
                        pstack[-1].append(obj)
                    else:
                        yield obj

        if pstack:
            raise Tilted("syntaxerror")

    def run(self) -> None:
        """Run the engine until it stops."""
        while self.estack:
            if callable(self.estack[-1]):
                func = self.estack.pop()
                func(self)
            else:
                try:
                    obj = next(self.estack[-1])
                except StopIteration:
                    self.estack.pop()
                    continue
                self.exec(obj, direct=True)

    def exec(self, obj: Object, direct: bool=False) -> None:
        """Execute one Stilted Object."""
        match obj:
            case Name(literal=False, value=name):
                looked_up = self.dstack_value(obj)
                if looked_up is None:
                    raise Tilted(f"undefined: {name}")
                self.exec(looked_up)

            case Array(literal=False):
                if direct:
                    self.opush(obj)
                else:
                    self.estack.append(iter(obj.value))

            case Operator():
                obj.value(self)

            case Object(literal=True):
                self.opush(obj)

            case _:
                raise Exception(f"Buh? {obj!r}")

    def run_name(self, name: str) -> None:
        """Run a name."""
        self.estack.append(iter([Name(False, name)]))

    ##
    ## Operand stack methods.
    ##

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

    def otop(self) -> Object:
        """Peek at the top object on the stack, or stackunderflow if empty."""
        self.ohas(1)
        return self.ostack[-1]

    def counttomark(self) -> int:
        """How deep is the nearest mark on the operand stack?"""
        for i, val in enumerate(reversed(self.ostack)):
            if val is MARK:
                return i
        raise Tilted("unmatchedmark")

    ##
    ## Compound object creation.
    ##

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

    ##
    ## Dict stack methods.
    ##

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

    ##
    ## Save object methods.
    ##

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

    def prep_for_change(self, obj: SaveableObject) -> None:
        """An object is about to change. Do save/restore bookkeeping."""
        obj.prep_for_change(self.sstack[-1])

    ##
    ## Graphics stack methods.
    ##

    @property
    def gctx(self):
        return self.device.ctx

    def gsave(self, from_save: bool) -> None:
        """Add a new gstate to the gstack."""
        self.gctx.save()
        self.gsaves.append(GstateExtras.from_ctx(from_save=from_save, ctx=self.gctx))

    def grestoreall(self) -> None:
        """Roll back the gstack to the last save."""
        if self.gsaves:
            while not self.gsaves[-1].from_save:
                self.gctx.restore()
                self.gsaves.pop()
            self.gsaves[-1].restore_to_ctx(self.gctx)


def evaluate(text: str, stdout=None) -> Engine:
    """A simple helper to execute text."""
    engine = Engine(stdout=stdout)
    engine.run_text(text)
    return engine


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


# Imported but not used, assert them to quiet the linter.  Import at the bottom
# of the file to avoid circular import problems.
import op_array; assert op_array
import op_collections; assert op_collections
import op_control; assert op_control
import op_dict; assert op_dict
import op_graphics; assert op_graphics
import op_math; assert op_math
import op_matrix; assert op_matrix
import op_object; assert op_object
import op_output; assert op_output
import op_relational; assert op_relational
import op_stack; assert op_stack
import op_string; assert op_string
import op_vm; assert op_vm
