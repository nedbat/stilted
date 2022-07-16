"""Built-in stack operators for stilted."""

from estate import operator, ExecState
from dtypes import MARK


@operator
def clear(estate: ExecState) -> None:
    estate.ostack.clear()

@operator
def cleartomark(estate: ExecState) -> None:
    n = estate.counttomark()
    del estate.ostack[-(n + 1):]

@operator
def copy(estate: ExecState) -> None:
    estate.ohas(1)
    if isinstance(estate.ostack[-1], int):
        n, = estate.opop(1)
        if n:
            estate.ohas(n)
            estate.ostack.extend(estate.ostack[-n:])

@operator
def count(estate: ExecState) -> None:
    estate.opush(len(estate.ostack))

@operator
def counttomark(estate: ExecState) -> None:
    estate.opush(estate.counttomark())

@operator("def")
def def_(estate: ExecState) -> None:
    name, val = estate.opop(2)
    estate.dstack[name.name] = val

@operator
def dup(estate: ExecState) -> None:
    estate.ohas(1)
    estate.opush(estate.ostack[-1])

@operator
def exch(estate: ExecState) -> None:
    a, b = estate.opop(2)
    estate.ostack.extend([b, a])

@operator
def index(estate: ExecState) -> None:
    n, = estate.opop(1)
    estate.opush(estate.ostack[-(n + 1)])

@operator
def mark(estate: ExecState) -> None:
    estate.opush(MARK)

@operator("[")
def mark_(estate: ExecState) -> None:
    estate.opush(MARK)

@operator
def pop(estate: ExecState) -> None:
    estate.opop(1)

@operator
def roll(estate: ExecState) -> None:
    n, j = estate.opop(2)
    vals = estate.opop(n)
    vals = vals[-j:] + vals[:-j]
    estate.ostack.extend(vals)
