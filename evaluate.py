"""Stack evaluation for stilted."""

from __future__ import annotations
from collections import ChainMap
from dataclasses import dataclass
from typing import Any

from lex import lexer, Name

@dataclass
class ExecState:
    """The PostScript execution state."""
    dstack: ChainMap
    ostack: list[Any]
    userdict: dict[str, Any]

    @classmethod
    def new(cls) -> ExecState:
        userdict: dict[str, Any] = {}
        return cls(
            dstack=ChainMap(userdict, SYSTEMDICT),
            ostack=[],
            userdict=userdict,
        )


# The `systemdict` dict for all builtin names.
SYSTEMDICT = {}


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


@builtin_with_name("def")
def def_(estate: ExecState) -> None:
    o = estate.ostack
    val, name = o.pop(), o.pop()
    estate.dstack[name.name] = val

@builtin
def dup(estate: ExecState) -> None:
    estate.ostack.append(estate.ostack[-1])

@builtin
def exch(estate: ExecState) -> None:
    o = estate.ostack
    a, b = o.pop(), o.pop()
    o.append(a)
    o.append(b)

@builtin
def pop(estate: ExecState) -> None:
    estate.ostack.pop()


def evaluate(text: str) -> ExecState:
    estate = ExecState.new()
    for tok in lexer.tokens(text):
        evaluate_one(tok, estate)

    return estate

def evaluate_one(obj: Any, estate: ExecState) -> None:
    match obj:
        case str() | int() | float():
            estate.ostack.append(obj)

        case Name(name, literal=True):
            estate.ostack.append(obj)

        case Name(name, literal=False):
            func = estate.dstack[name]
            evaluate_one(func, estate)

        case _ if callable(obj):
            obj(estate)

        case _:
            raise Exception(f"Buh? {obj!r}")
