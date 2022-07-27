"""Built-in string operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import Integer, String

@operator
def string(estate: ExecState) -> None:
    n = estate.opop(Integer)
    if n.value < 0:
        raise Tilted("rangecheck")
    estate.opush(String.from_size(n.value))
