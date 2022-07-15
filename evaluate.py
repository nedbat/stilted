"""Stack evaluation for stilted."""

from dataclasses import dataclass
from typing import Any

from lex import lexer, Name

@dataclass
class ExecState:
    """The PostScript execution state."""
    dstack: list[dict[str, Any]]
    ostack: list[Any]

    @classmethod
    def new(cls):
        return cls(dstack=[SYSTEMDICT], ostack=[])


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


def evaluate(text: str) -> list[Any]:
    estate = ExecState.new()

    for tok in lexer.tokens(text):
        match tok:
            case str() | int() | float():
                estate.ostack.append(tok)

            case Name(name, literal=True):
                estate.ostack.append(tok)

            case Name(name, literal=False):
                func = SYSTEMDICT[name]
                func(estate)

            case _:
                raise Exception(f"Buh? {tok!r}")

    return estate.ostack
