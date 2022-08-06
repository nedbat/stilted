"""Built-in stack operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import (
    from_py, rangecheck, typecheck,
    Array, Dict, Integer, MARK, String,
)


@operator
def clear(estate: ExecState) -> None:
    estate.ostack.clear()

@operator
def cleartomark(estate: ExecState) -> None:
    n = estate.counttomark()
    del estate.ostack[-(n + 1):]

@operator
def copy(estate: ExecState) -> None:
    if isinstance(estate.otop(), Integer):
        n = estate.opop().value
        rangecheck(0, n)
        if n > 0:
            estate.ohas(n)
            estate.opush(*estate.ostack[-n:])
    else:
        obj1, obj2 = estate.opopn(2)
        match obj1, obj2:
            case Dict(), Dict():
                estate.prep_for_change(obj2)
                for k, v in obj1.value.items():
                    obj2[k] = v
                estate.opush(obj2)

            case (Array(), Array()) | (String(), String()):
                rangecheck(obj1.length, obj2.length)
                for i in range(obj1.length):
                    obj2[i] = obj1[i]
                estate.opush(obj2.new_sub(0, obj1.length))

            case _:
                raise Tilted(f"typecheck: got {type(obj1)}, {type(obj2)}")

@operator
def count(estate: ExecState) -> None:
    estate.opush(from_py(len(estate.ostack)))

@operator
def counttomark(estate: ExecState) -> None:
    estate.opush(from_py(estate.counttomark()))

@operator
def dup(estate: ExecState) -> None:
    estate.opush(estate.otop())

@operator
def exch(estate: ExecState) -> None:
    a, b = estate.opopn(2)
    estate.opush(b, a)

@operator
def index(estate: ExecState) -> None:
    n = estate.opop(Integer)
    estate.ohas(n.value + 1)
    rangecheck(0, n.value)
    estate.opush(estate.ostack[-(n.value + 1)])

@operator
def mark(estate: ExecState) -> None:
    estate.opush(MARK)

@operator
def pop(estate: ExecState) -> None:
    estate.opop()

@operator
def roll(estate: ExecState) -> None:
    n, j = estate.opopn(2)
    typecheck(Integer, n, j)
    vals = estate.opopn(n.value)
    estate.opush(*vals[-j.value:])
    estate.opush(*vals[:-j.value])
