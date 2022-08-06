"""Built-in dict operators for stilted."""

from error import Tilted
from evaluate import operator, Engine
from dtypes import from_py, rangecheck, typecheck, Dict, Integer, Stringy

@operator
def begin(engine: Engine) -> None:
    d = engine.opop(Dict)
    engine.dstack.append(d)

@operator
def cleardictstack(engine: Engine) -> None:
    while len(engine.dstack) > 2:
        engine.dstack.pop()

@operator
def countdictstack(engine: Engine) -> None:
    engine.opush(from_py(len(engine.dstack)))

@operator
def currentdict(engine: Engine) -> None:
    engine.opush(engine.dstack[-1])

@operator("dict")
def dict_(engine: Engine) -> None:
    n = engine.opop(Integer)
    rangecheck(0, n.value)
    engine.opush(engine.new_dict())

@operator("def")
def def_(engine: Engine) -> None:
    name, val = engine.opopn(2)
    typecheck(Stringy, name)
    d = engine.dstack[-1]
    engine.prep_for_change(d)
    d[name.str_value] = val

@operator
def end(engine: Engine) -> None:
    if len(engine.dstack) <= 2:
        raise Tilted("dictstackunderflow")
    engine.dstack.pop()

@operator
def known(engine: Engine) -> None:
    d, k = engine.opopn(2)
    typecheck(Dict, d)
    typecheck(Stringy, k)
    engine.opush(from_py(k.str_value in d.value))

@operator
def load(engine: Engine) -> None:
    k = engine.opop(Stringy)
    obj = engine.dstack_value(k)
    if obj is None:
        raise Tilted(f"undefined: {k.str_value}")
    engine.opush(obj)

@operator
def maxlength(engine: Engine) -> None:
    d = engine.opop(Dict)
    engine.opush(from_py(len(d.value) + 10))

@operator
def store(engine: Engine) -> None:
    k, o = engine.opopn(2)
    typecheck(Stringy, k)
    d = engine.dstack_dict(k)
    if d is None:
        d = engine.dstack[-1]
    engine.prep_for_change(d)
    d[k.str_value] = o

@operator
def where(engine: Engine) -> None:
    k = engine.opop(Stringy)
    d = engine.dstack_dict(k)
    if d is not None:
        engine.opush(d, from_py(True))
    else:
        engine.opush(from_py(False))
