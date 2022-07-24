"""Built-in math operators for stilted."""

import math

from estate import operator, ExecState
from dtypes import from_py, typecheck, Number


@operator("abs")
def abs_(estate: ExecState) -> None:
    a = estate.opop()
    typecheck(Number, a)
    estate.opush(from_py(abs(a.value)))

@operator
def add(estate: ExecState) -> None:
    a, b = estate.opopn(2)
    typecheck(Number, a, b)
    estate.opush(from_py(a.value + b.value))

@operator
def ceiling(estate: ExecState) -> None:
    a = estate.opop()
    typecheck(Number, a)
    av = a.value
    estate.opush(from_py(type(av)(math.ceil(av))))

@operator
def div(estate: ExecState) -> None:
    a, b = estate.opopn(2)
    typecheck(Number, a, b)
    estate.opush(from_py(a.value / b.value))

@operator
def floor(estate: ExecState) -> None:
    a = estate.opop()
    typecheck(Number, a)
    av = a.value
    estate.opush(from_py(type(av)(math.floor(av))))

@operator
def idiv(estate: ExecState) -> None:
    a, b = estate.opopn(2)
    typecheck(Number, a, b)
    estate.opush(from_py(int(a.value / b.value)))

@operator
def mod(estate: ExecState) -> None:
    a, b = estate.opopn(2)
    typecheck(Number, a, b)
    av, bv = a.value, b.value
    remainder = (-1 if av < 0 else 1) * (abs(av) % abs(bv))
    estate.opush(from_py(remainder))

@operator
def mul(estate: ExecState) -> None:
    a, b = estate.opopn(2)
    typecheck(Number, a, b)
    estate.opush(from_py(a.value * b.value))

@operator
def neg(estate: ExecState) -> None:
    a = estate.opop()
    typecheck(Number, a)
    estate.opush(from_py(-a.value))

@operator("round")
def round_(estate: ExecState) -> None:
    a = estate.opop()
    typecheck(Number, a)
    av = a.value
    if av - int(av) == 0.5:
        r = int(av) + 1
    else:
        r = round(av)
    estate.opush(from_py(type(av)(r)))

@operator
def sub(estate: ExecState) -> None:
    a, b = estate.opopn(2)
    typecheck(Number, a, b)
    estate.opush(from_py(a.value - b.value))

@operator
def truncate(estate: ExecState) -> None:
    a = estate.opop()
    typecheck(Number, a)
    av = a.value
    estate.opush(from_py(type(av)(math.trunc(av))))
