"""Stack evaluation for stilted."""

from __future__ import annotations

import itertools
import random
import sys
from dataclasses import dataclass
from typing import Any, Iterable, Iterator, cast

from error import ERROR_NAMES, Tilted
from lex import lexer
from dtypes import (
    from_py, typecheck,
    Array, ArrayStorage, Boolean, Dict, DictStorage, Integer,
    MARK, Mark, Name, NULL, Null,
    Object, Operator, Real, Save, SaveableObject, String,
)
from gstate import Device, GstateExtras


class Engine:
    """Stilted execution engine."""

    # Operand stack
    ostack: list[Object]

    # Dictionary stack
    dstack: list[Dict]

    # Objects popped by the current operator, so they can be put back for error
    # handling if needed.
    popped: list[Object]

    # Execution stack. This is a mix of:
    #   1) Iterators of Stilted Objects (procedures)
    #   2) Python callables (used for internal work)
    estack: list[Any]

    # Save-object stack
    sstack: list[Save]

    # gsave stack
    # Most of the graphics state is in PyCairo, but we need other information
    # for each gstate.
    gsaves: list[GstateExtras]

    # Random number source
    random: random.Random

    # The stdout file object
    stdout: Any

    # Sequence of serial numbers for save objects
    save_serials: Iterator[int]

    # Output device
    device: Device

    def __init__(self, stdout=None, outfile="page.svg") -> None:
        """Construct the initial data needed for execution."""
        self.ostack = []
        self.dstack = []
        self.estack = []
        self.sstack = []
        self.gsaves = []

        self.popped = []

        self.random = random.Random()

        self.stdout = stdout or sys.stdout
        self.save_serials = itertools.count()
        self.device = Device(outfile)

        self.new_save()

        systemdict = self.new_dict(value=SYSTEMDICT)
        systemdict["systemdict"] = systemdict
        self.dstack.append(systemdict)

        systemdict["$error"] = self.new_dict()
        systemdict["errordict"] = self.new_dict()
        for err_name in ERROR_NAMES:
            self.exec_text(
                f"errordict /{err_name} {{ /{err_name} .error }} put"
            )

        self.exec_text("""
            /=string 150 string def     % Not standardized, but expected.
            /languagelevel 1 def
            /product (Stilted) def
            /version (0.0) def
            """)

        userdict = self.new_dict()
        systemdict["userdict"] = userdict
        self.dstack.append(userdict)

    def add_text(self, text: str) -> None:
        """Consume text as Stilted tokens, and add for execution."""
        self.estack.append(self._collect_objects(lexer.tokens(text)))

    def exec_text(self, text: str) -> None:
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
                    proc = self.new_array(value=pstack.pop(), literal=False)
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
                except Tilted as tilt:
                    # An error!
                    self._handle_error(obj, tilt)
                else:
                    self.exec(obj, direct=True)

    def exec(self, obj: Object, direct: bool=False) -> None:
        """Execute one Stilted Object."""
        self.popped = []

        try:
            match obj:
                # PSRM §3.5.5
                case Object(literal=True):
                    self.opush(obj)

                # Below here are all executable cases:

                case Array():
                    if direct:
                        self.opush(obj)
                    else:
                        self.estack.append(iter(obj.value))

                case Integer() | Real() | Boolean() | Mark():
                    self.opush(obj)

                case Name():
                    looked_up = self.dstack_value(obj)
                    if looked_up is None:
                        raise Tilted("undefined")
                    self.exec(looked_up)

                case Null():
                    pass

                case Operator():
                    obj.value(self)

                case String():
                    self.add_text(obj.str_value)

                case _:
                    raise Exception(f"Buh? {obj!r}")

        except Tilted as tilt:
            # An error!
            self._handle_error(obj, tilt)

    def _handle_error(self, obj: Object, tilt: Tilted) -> None:
        """Handle an error: §3.11.1"""
        # Put back what was popped, push the object,
        # find the error name in `errordict`, and execute it.
        self.opush(*self.popped[::-1])
        self.opush(obj)
        errordict = self.builtin_dict("errordict")
        handler = errordict[tilt.errname]
        self.exec(handler)

    def exec_name(self, name: str) -> None:
        """Run a name."""
        self.exec(Name(False, name))

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
        self.popped.append(obj)
        if a_type is not None:
            typecheck(a_type, obj)
        return obj

    def opopn(self, n: int, a_type=None) -> list[Any]:
        """
        Remove the top n operands and return them.

        Optionally typecheck all the values with `a_type`.
        """
        self.ohas(n)
        if n == 0:
            vals = []
            return []

        vals = self.ostack[-n:]
        if a_type is not None:
            typecheck(a_type, *vals)
        del self.ostack[-n:]
        self.popped.extend(vals[::-1])
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

    def pstack(self, stack: list[Object]) -> None:
        """Print a stack to stdout."""
        if self.stdout is not None:
            for obj in reversed(stack):
                self.stdout.write(obj.op_eqeq())
                self.stdout.write("\n")

    ##
    ## Compound object creation.
    ##

    def new_array(
        self,
        n: int=None,
        value: list[Object]=None,
        literal:bool=True,
    ) -> Array:
        """Make a new Array, either by size or contents."""
        if value is None:
            assert n is not None
            value = [NULL] * n
        else:
            n = len(value)
        return Array(
            literal=literal,
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

    def builtin_dict(self, name: str) -> Dict:
        """Get one of the builtin dicts"""
        return cast(Dict, self.dstack[0][name])

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


@dataclass
class Exitable:
    """An item on the execstack that can be `exit`ed."""
    exitable = True


def evaluate(text: str, stdout=None) -> Engine:
    """A simple helper to execute text."""
    engine = Engine(stdout=stdout)
    engine.push_string(text)
    engine.exec_text("cvx stopped { $error /errorname get .pyraise } if")
    return engine


def operator(arg):
    """
    Define a built-in operator.

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


# The `systemdict` dict for all builtin names.
SYSTEMDICT: dict[str, Object] = {}

SYSTEMDICT["false"] = from_py(False)
SYSTEMDICT["null"] = from_py(None)
SYSTEMDICT["true"] = from_py(True)


# Imported but not used, assert them to quiet the linter.
# Import at the bottom of the file to avoid circular import problems.
import op_array; assert op_array
import op_collections; assert op_collections
import op_control; assert op_control
import op_dict; assert op_dict
import op_error; assert op_error
import op_font; assert op_font
import op_gstate; assert op_gstate
import op_math; assert op_math
import op_matrix; assert op_matrix
import op_misc; assert op_misc
import op_output; assert op_output
import op_paint; assert op_paint
import op_path; assert op_path
import op_relational; assert op_relational
import op_stack; assert op_stack
import op_string; assert op_string
import op_type; assert op_type
import op_vm; assert op_vm
