"""Built-in math operators for stilted."""

import math

from error import Tilted
from estate import operator, ExecState
from dtypes import Number

def numbers(*vals) -> None:
    """Check that all the arguments are numbers."""
    for val in vals:
        if not isinstance(val, Number):
            raise Tilted("typecheck")

@operator("abs")
def abs_(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.opush(abs(a))

@operator
def add(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.opush(a + b)

@operator
def ceiling(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.opush(type(a)(math.ceil(a)))

@operator
def div(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.opush(a / b)

@operator
def floor(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.opush(type(a)(math.floor(a)))

@operator
def idiv(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.opush(int(a / b))

@operator
def mod(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    remainder = (-1 if a < 0 else 1) * (abs(a) % abs(b))
    estate.opush(remainder)

@operator
def mul(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.opush(a * b)

@operator
def neg(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.opush(-a)

@operator("round")
def round_(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    if a - int(a) == 0.5:
        r = int(a) + 1
    else:
        r = round(a)
    estate.opush(type(a)(r))

@operator
def sub(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.opush(a - b)

@operator
def truncate(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.opush(type(a)(math.trunc(a)))
