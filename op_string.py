"""Built-in string operators for Stilted."""

from evaluate import operator, Engine
from dtypes import rangecheck, Integer, String

@operator
def string(engine: Engine) -> None:
    n = engine.opop(Integer)
    rangecheck(0, n.value)
    engine.opush(String.from_size(n.value))
