"""Built-in dict operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import from_py, typecheck, Dict, Integer, Name, Stringy

@operator
def begin(estate: ExecState) -> None:
    d = estate.opop()
    typecheck(Dict, d)
    estate.dstack.append(d)

@operator
def countdictstack(estate: ExecState) -> None:
    estate.opush(from_py(len(estate.dstack)))

@operator("dict")
def dict_(estate: ExecState) -> None:
    n = estate.opop()
    typecheck(Integer, n)
    if n.value < 0:
        raise Tilted("rangecheck")
    estate.opush(estate.new_dict())

@operator
def currentdict(estate: ExecState) -> None:
    estate.opush(estate.dstack[-1])

@operator("def")
def def_(estate: ExecState) -> None:
    name, val = estate.opopn(2)
    typecheck(Name, name)
    estate.dstack[-1][name.value] = val

@operator
def end(estate: ExecState) -> None:
    if len(estate.dstack) <= 2:
        raise Tilted("dictstackunderflow")
    estate.dstack.pop()

@operator
def load(estate: ExecState) -> None:
    k = estate.opop()
    typecheck(Stringy, k)
    obj = estate.dstack_value(k)
    if obj is None:
        raise Tilted(f"undefined: {k.value}")
    estate.opush(obj)

@operator
def known(estate: ExecState) -> None:
    d, k = estate.opopn(2)
    typecheck(Dict, d)
    typecheck(Stringy, k)
    estate.opush(from_py(k.value in d.value))

@operator
def store(estate: ExecState) -> None:
    k, o = estate.opopn(2)
    typecheck(Stringy, k)
    d = estate.dstack_dict(k)
    if d is None:
        d = estate.dstack[-1]
    d[k.value] = o

@operator
def where(estate: ExecState) -> None:
    k = estate.opop()
    typecheck(Stringy, k)
    d = estate.dstack_dict(k)
    if d is not None:
        estate.opush(d, from_py(True))
    else:
        estate.opush(from_py(False))
