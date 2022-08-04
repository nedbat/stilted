"""Built-in dict operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import from_py, rangecheck, typecheck, Dict, Integer, Stringy

@operator
def begin(estate: ExecState) -> None:
    d = estate.opop(Dict)
    estate.dstack.append(d)

@operator
def cleardictstack(estate: ExecState) -> None:
    while len(estate.dstack) > 2:
        estate.dstack.pop()

@operator
def countdictstack(estate: ExecState) -> None:
    estate.opush(from_py(len(estate.dstack)))

@operator
def currentdict(estate: ExecState) -> None:
    estate.opush(estate.dstack[-1])

@operator("dict")
def dict_(estate: ExecState) -> None:
    n = estate.opop(Integer)
    rangecheck(0, n.value)
    estate.opush(estate.new_dict())

@operator("def")
def def_(estate: ExecState) -> None:
    name, val = estate.opopn(2)
    typecheck(Stringy, name)
    d = estate.dstack[-1]
    estate.prep_for_change(d)
    d[name.str_value] = val

@operator
def end(estate: ExecState) -> None:
    if len(estate.dstack) <= 2:
        raise Tilted("dictstackunderflow")
    estate.dstack.pop()

@operator
def known(estate: ExecState) -> None:
    d, k = estate.opopn(2)
    typecheck(Dict, d)
    typecheck(Stringy, k)
    estate.opush(from_py(k.str_value in d.value))

@operator
def load(estate: ExecState) -> None:
    k = estate.opop(Stringy)
    obj = estate.dstack_value(k)
    if obj is None:
        raise Tilted(f"undefined: {k.str_value}")
    estate.opush(obj)

@operator
def maxlength(estate: ExecState) -> None:
    d = estate.opop(Dict)
    estate.opush(from_py(len(d.value) + 10))

@operator
def store(estate: ExecState) -> None:
    k, o = estate.opopn(2)
    typecheck(Stringy, k)
    d = estate.dstack_dict(k)
    if d is None:
        d = estate.dstack[-1]
    estate.prep_for_change(d)
    d[k.str_value] = o

@operator
def where(estate: ExecState) -> None:
    k = estate.opop(Stringy)
    d = estate.dstack_dict(k)
    if d is not None:
        estate.opush(d, from_py(True))
    else:
        estate.opush(from_py(False))
