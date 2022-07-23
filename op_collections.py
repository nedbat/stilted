"""Built-in collections operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import from_py, typecheck, Dict, Stringy

@operator
def get(estate: ExecState) -> None:
    d, k = estate.opop(2)
    typecheck(Dict, d)
    typecheck(Stringy, k)
    try:
        obj = d.value[k.value]
    except KeyError:
        raise Tilted(f"undefined: {k.value}")
    estate.opush(obj)

@operator
def length(estate: ExecState) -> None:
    d = estate.opop(1)[0]
    typecheck(Dict, d)
    estate.opush(from_py(len(d.value)))

@operator
def put(estate: ExecState) -> None:
    d, k, o = estate.opop(3)
    typecheck(Dict, d)
    typecheck(Stringy, k)
    d.value[k.value] = o
