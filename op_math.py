"""Built-in math operators for stilted."""

import math

from error import Tilted
from estate import builtin, builtin_with_name, ExecState
from pstypes import number

def numbers(*vals) -> None:
    """Check that all the arguments are numbers."""
    for val in vals:
        if not isinstance(val, number):
            raise Tilted("typecheck")

@builtin_with_name("abs")
def abs_(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.ostack.append(abs(a))

@builtin
def add(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.ostack.append(a + b)

@builtin
def ceiling(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.ostack.append(type(a)(math.ceil(a)))

@builtin
def div(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.ostack.append(a / b)

@builtin
def floor(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.ostack.append(type(a)(math.floor(a)))

@builtin
def idiv(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.ostack.append(int(a / b))

@builtin
def mod(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    remainder = (-1 if a < 0 else 1) * (abs(a) % abs(b))
    estate.ostack.append(remainder)

@builtin
def mul(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.ostack.append(a * b)

@builtin
def neg(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.ostack.append(-a)

@builtin_with_name("round")
def round_(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    if a - int(a) == 0.5:
        r = int(a) + 1
    else:
        r = round(a)
    estate.ostack.append(type(a)(r))

@builtin
def sub(estate: ExecState) -> None:
    a, b = estate.opop(2)
    numbers(a, b)
    estate.ostack.append(a - b)

@builtin
def truncate(estate: ExecState) -> None:
    a, = estate.opop(1)
    numbers(a)
    estate.ostack.append(type(a)(math.trunc(a)))
