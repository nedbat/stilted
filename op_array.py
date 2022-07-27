"""Built-in array operators for stilted."""

from estate import operator, ExecState
from dtypes import rangecheck, Integer, MARK

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
def array(estate: ExecState) -> None:
    n = estate.opop(Integer).value
    rangecheck(0, n)
    estate.opush(estate.new_array(n=n))
