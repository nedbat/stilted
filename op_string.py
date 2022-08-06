"""Built-in string operators for stilted."""

from evaluate import operator, Engine
from dtypes import rangecheck, typecheck, Integer, Name, String

@operator
def cvn(engine: Engine) -> None:
    s = engine.opop(String)
    engine.opush(Name(literal=s.literal, value=s.str_value))

@operator
def cvs(engine: Engine) -> None:
    obj, s = engine.opopn(2)
    typecheck(String, s)
    eqs = obj.op_eq().encode("iso8859-1")
    rangecheck(len(eqs), s.length)
    for i in range(len(eqs)):
        s[i] = eqs[i]
    engine.opush(s.new_sub(0, len(eqs)))

@operator
def string(engine: Engine) -> None:
    n = engine.opop(Integer)
    rangecheck(0, n.value)
    engine.opush(String.from_size(n.value))
