"""Built-in stack operators for stilted."""

from error import Tilted
from estate import builtin, builtin_with_name, ExecState
from pstypes import MARK


@builtin
def clear(estate: ExecState) -> None:
    estate.ostack.clear()

@builtin
def cleartomark(estate: ExecState) -> None:
    n = estate.counttomark()
    del estate.ostack[-(n + 1):]

@builtin
def copy(estate: ExecState) -> None:
    estate.ohas(1)
    if isinstance(estate.ostack[-1], int):
        n, = estate.opop(1)
        if n:
            estate.ohas(n)
            estate.ostack.extend(estate.ostack[-n:])

@builtin
def count(estate: ExecState) -> None:
    estate.ostack.append(len(estate.ostack))

@builtin
def counttomark(estate: ExecState) -> None:
    estate.ostack.append(estate.counttomark())

@builtin_with_name("def")
def def_(estate: ExecState) -> None:
    name, val = estate.opop(2)
    estate.dstack[name.name] = val

@builtin
def dup(estate: ExecState) -> None:
    estate.ohas(1)
    estate.ostack.append(estate.ostack[-1])

@builtin
def exch(estate: ExecState) -> None:
    a, b = estate.opop(2)
    estate.ostack.extend([b, a])

@builtin
def index(estate: ExecState) -> None:
    n, = estate.opop(1)
    estate.ostack.append(estate.ostack[-(n + 1)])

@builtin
def mark(estate: ExecState) -> None:
    estate.ostack.append(MARK)

@builtin_with_name("[")
def mark_(estate: ExecState) -> None:
    estate.ostack.append(MARK)

@builtin
def pop(estate: ExecState) -> None:
    estate.opop(1)

@builtin
def roll(estate: ExecState) -> None:
    n, j = estate.opop(2)
    vals = estate.opop(n)
    vals = vals[-j:] + vals[:-j]
    estate.ostack.extend(vals)
