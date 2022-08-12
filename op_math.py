"""Built-in math operators for stilted."""

import math

from error import Tilted
from evaluate import operator, Engine
from dtypes import from_py, typecheck, Integer, Number


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
def exp(engine: Engine) -> None:
    base, exponent = engine.opopn(2)
    typecheck(Number, base, exponent)
    val = base.value ** exponent.value
    engine.opush(from_py(val))

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

@operator
def rand(engine: Engine) -> None:
    engine.opush(from_py(engine.random.randint(0, 2**31-1)))

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
def rrand(engine: Engine) -> None:
    r = engine.random.randint(0, 2**31-1)
    engine.random.seed(r)
    engine.opush(from_py(r))

@operator
def sqrt(engine: Engine) -> None:
    num = engine.opop(Number)
    try:
        res = math.sqrt(num.value)
    except ValueError:
        raise Tilted("rangecheck")
    engine.opush(from_py(res))

@operator
def srand(engine: Engine) -> None:
    i = engine.opop(Integer)
    engine.random.seed(i.value)

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
