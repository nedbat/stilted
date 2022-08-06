"""Built-in array operators for stilted."""

from evaluate import operator, Engine
from dtypes import rangecheck, Array, Integer, MARK

@operator("[")
def mark_(engine: Engine) -> None:
    engine.opush(MARK)

@operator("]")
def array_(engine: Engine) -> None:
    n = engine.counttomark()
    objs = engine.opopn(n)
    engine.opop() # the mark
    engine.opush(engine.new_array(value=objs))

@operator
def aload(engine: Engine) -> None:
    arr = engine.opop(Array)
    for obj in arr:
        engine.opush(obj)
    engine.opush(arr)

@operator
def array(engine: Engine) -> None:
    n = engine.opop(Integer).value
    rangecheck(0, n)
    engine.opush(engine.new_array(n=n))

@operator
def astore(engine: Engine) -> None:
    arr = engine.opop(Array)
    larr = len(arr)
    engine.ohas(larr)
    for i in range(larr):
        arr[larr - i - 1] = engine.opop()
    engine.opush(arr)
