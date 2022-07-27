"""Built-in string operators for stilted."""

from estate import operator, ExecState
from dtypes import rangecheck, Integer, String

@operator
def string(estate: ExecState) -> None:
    n = estate.opop(Integer)
    rangecheck(0, n.value)
    estate.opush(String.from_size(n.value))
