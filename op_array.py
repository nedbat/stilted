"""Built-in array operators for stilted."""

from estate import operator, ExecState
from dtypes import rangecheck, Array, Integer, MARK

@operator("[")
def mark_(estate: ExecState) -> None:
    estate.opush(MARK)

@operator("]")
def array_(estate: ExecState) -> None:
    n = estate.counttomark()
    objs = estate.opopn(n)
    estate.opop() # the mark
    estate.opush(estate.new_array(value=objs))

@operator
def aload(estate: ExecState) -> None:
    arr = estate.opop(Array)
    for obj in arr:
        estate.opush(obj)
    estate.opush(arr)

@operator
def array(estate: ExecState) -> None:
    n = estate.opop(Integer).value
    rangecheck(0, n)
    estate.opush(estate.new_array(n=n))

@operator
def astore(estate: ExecState) -> None:
    arr = estate.opop(Array)
    larr = len(arr)
    estate.ohas(larr)
    for i in range(larr):
        arr[larr - i - 1] = estate.opop()
    estate.opush(arr)
