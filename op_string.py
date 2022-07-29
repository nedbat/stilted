"""Built-in string operators for stilted."""

from estate import operator, ExecState
from dtypes import rangecheck, typecheck, Integer, Name, String

@operator
def cvn(estate: ExecState) -> None:
    s = estate.opop(String)
    estate.opush(Name(literal=s.literal, value=s.str_value))

@operator
def cvs(estate: ExecState) -> None:
    obj, s = estate.opopn(2)
    typecheck(String, s)
    eqs = obj.op_eq().encode("iso8859-1")
    rangecheck(len(eqs), s.length)
    for i in range(len(eqs)):
        s[i] = eqs[i]
    estate.opush(s.new_sub(0, len(eqs)))

@operator
def string(estate: ExecState) -> None:
    n = estate.opop(Integer)
    rangecheck(0, n.value)
    estate.opush(String.from_size(n.value))
