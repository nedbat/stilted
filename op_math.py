"""Built-in math operators for stilted."""

import math

from evaluate import operator, Engine
from dtypes import from_py, typecheck, Number


@operator("abs")
def abs_(engine: Engine) -> None:
    a = engine.opop(Number)
    engine.opush(from_py(abs(a.value)))

@operator
def add(engine: Engine) -> None:
    a, b = engine.opopn(2)
    typecheck(Number, a, b)
    engine.opush(from_py(a.value + b.value))

@operator
def ceiling(engine: Engine) -> None:
    a = engine.opop(Number)
    av = a.value
    engine.opush(from_py(type(av)(math.ceil(av))))

@operator
def div(engine: Engine) -> None:
    a, b = engine.opopn(2)
    typecheck(Number, a, b)
    engine.opush(from_py(a.value / b.value))

@operator
def floor(engine: Engine) -> None:
    a = engine.opop(Number)
    av = a.value
    engine.opush(from_py(type(av)(math.floor(av))))

@operator
def idiv(engine: Engine) -> None:
    a, b = engine.opopn(2)
    typecheck(Number, a, b)
    engine.opush(from_py(int(a.value / b.value)))

@operator
def mod(engine: Engine) -> None:
    a, b = engine.opopn(2)
    typecheck(Number, a, b)
    av, bv = a.value, b.value
    remainder = (-1 if av < 0 else 1) * (abs(av) % abs(bv))
    engine.opush(from_py(remainder))

@operator
def mul(engine: Engine) -> None:
    a, b = engine.opopn(2)
    typecheck(Number, a, b)
    engine.opush(from_py(a.value * b.value))

@operator
def neg(engine: Engine) -> None:
    a = engine.opop(Number)
    engine.opush(from_py(-a.value))

@operator("round")
def round_(engine: Engine) -> None:
    a = engine.opop(Number)
    av = a.value
    if av - int(av) == 0.5:
        r = int(av) + 1
    else:
        r = round(av)
    engine.opush(from_py(type(av)(r)))

@operator
def sub(engine: Engine) -> None:
    a, b = engine.opopn(2)
    typecheck(Number, a, b)
    engine.opush(from_py(a.value - b.value))

@operator
def truncate(engine: Engine) -> None:
    a = engine.opop(Number)
    av = a.value
    engine.opush(from_py(type(av)(math.trunc(av))))
