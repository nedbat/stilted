"""Built-in dict operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import from_py, typecheck, Dict, Integer, Name, Stringy

@operator
def begin(estate: ExecState) -> None:
    d = estate.opop(1)[0]
    typecheck(Dict, d)
    estate.dstack.maps.insert(0, d.value)

@operator
def countdictstack(estate: ExecState) -> None:
    estate.opush(from_py(len(estate.dstack.maps)))

@operator("dict")
def dict_(estate: ExecState) -> None:
    n = estate.opop(1)[0]
    typecheck(Integer, n)
    if n.value < 0:
        raise Tilted("rangecheck")
    estate.opush(from_py({}))

@operator
def currentdict(estate: ExecState) -> None:
    estate.opush(from_py(estate.dstack.maps[0]))

@operator("def")
def def_(estate: ExecState) -> None:
    name, val = estate.opop(2)
    typecheck(Name, name)
    estate.dstack[name.value] = val

@operator
def end(estate: ExecState) -> None:
    if len(estate.dstack.maps) <= 2:
        raise Tilted("dictstackunderflow")
    del estate.dstack.maps[0]

@operator
def load(estate: ExecState) -> None:
    k = estate.opop(1)[0]
    typecheck(Stringy, k)
    try:
        obj = estate.dstack[k.value]
    except KeyError:
        raise Tilted(f"undefined: {k.value}")
    estate.opush(obj)

@operator
def known(estate: ExecState) -> None:
    d, k = estate.opop(2)
    typecheck(Dict, d)
    typecheck(Stringy, k)
    estate.opush(from_py(k.value in d.value))

@operator
def store(estate: ExecState) -> None:
    k, o = estate.opop(2)
    typecheck(Stringy, k)
    for d in reversed(estate.dstack.maps):
        if k.value in d:
            break
    else:
        d = estate.dstack.maps[0]
    d[k.value] = o

@operator
def userdict(estate: ExecState) -> None:
    estate.opush(Dict(False, estate.userdict))

@operator
def where(estate: ExecState) -> None:
    k = estate.opop(1)[0]
    typecheck(Stringy, k)
    for d in reversed(estate.dstack.maps):
        if k.value in d:
            estate.opush(Dict(True, d), from_py(True))
            break
    else:
        estate.opush(from_py(False))
