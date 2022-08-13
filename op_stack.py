"""Built-in stack operators for stilted."""

from error import Tilted
from evaluate import operator, Engine
from dtypes import (
    from_py, typecheck,
    Array, Dict, Integer, MARK, String,
)
from util import rangecheck


@operator
def clear(engine: Engine) -> None:
    engine.ostack.clear()

@operator
def cleartomark(engine: Engine) -> None:
    n = engine.counttomark()
    del engine.ostack[-(n + 1):]

@operator
def copy(engine: Engine) -> None:
    if isinstance(engine.otop(), Integer):
        n = engine.opop().value
        rangecheck(0, n)
        if n > 0:
            engine.ohas(n)
            engine.opush(*engine.ostack[-n:])
    else:
        obj1, obj2 = engine.opopn(2)
        match obj1, obj2:
            case Dict(), Dict():
                engine.prep_for_change(obj2)
                for k, v in obj1.value.items():
                    obj2[k] = v
                engine.opush(obj2)

            case (Array(), Array()) | (String(), String()):
                rangecheck(obj1.length, obj2.length)
                for i in range(obj1.length):
                    obj2[i] = obj1[i]
                engine.opush(obj2.new_sub(0, obj1.length))

            case _:
                raise Tilted("typecheck", f"got {type(obj1)}, {type(obj2)}")

@operator
def count(engine: Engine) -> None:
    engine.opush(from_py(len(engine.ostack)))

@operator
def counttomark(engine: Engine) -> None:
    engine.opush(from_py(engine.counttomark()))

@operator
def dup(engine: Engine) -> None:
    engine.opush(engine.otop())

@operator
def exch(engine: Engine) -> None:
    a, b = engine.opopn(2)
    engine.opush(b, a)

@operator
def index(engine: Engine) -> None:
    n = engine.opop(Integer)
    engine.ohas(n.value + 1)
    rangecheck(0, n.value)
    engine.opush(engine.ostack[-(n.value + 1)])

@operator
def mark(engine: Engine) -> None:
    engine.opush(MARK)

@operator
def pop(engine: Engine) -> None:
    engine.opop()

@operator
def roll(engine: Engine) -> None:
    n, j = engine.opopn(2)
    typecheck(Integer, n, j)
    vals = engine.opopn(n.value)
    engine.opush(*vals[-j.value:])
    engine.opush(*vals[:-j.value])
