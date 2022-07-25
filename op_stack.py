"""Built-in stack operators for stilted."""

from estate import operator, ExecState
from dtypes import from_py, typecheck, Integer, MARK


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
    if isinstance(estate.ostack[-1], Integer):
        n = estate.opop().value
        if n:
            estate.ohas(n)
            estate.opush(*estate.ostack[-n:])

@operator
def count(estate: ExecState) -> None:
    estate.opush(from_py(len(estate.ostack)))

@operator
def counttomark(estate: ExecState) -> None:
    estate.opush(from_py(estate.counttomark()))

@operator
def dup(estate: ExecState) -> None:
    estate.ohas(1)
    estate.opush(estate.ostack[-1])

@operator
def exch(estate: ExecState) -> None:
    a, b = estate.opopn(2)
    estate.opush(b, a)

@operator
def index(estate: ExecState) -> None:
    n = estate.opop(Integer)
    estate.opush(estate.ostack[-(n.value + 1)])

@operator
def mark(estate: ExecState) -> None:
    estate.opush(MARK)

@operator("[")
def mark_(estate: ExecState) -> None:
    estate.opush(MARK)

@operator
def pop(estate: ExecState) -> None:
    estate.opop()

@operator
def roll(estate: ExecState) -> None:
    n, j = estate.opopn(2)
    vals = estate.opopn(n.value)
    estate.opush(*vals[-j.value:])
    estate.opush(*vals[:-j.value])
