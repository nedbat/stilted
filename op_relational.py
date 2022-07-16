"""Built-in relational operators for stilted."""

import operator as py_operator
from typing import Any, Callable

from error import Tilted
from estate import operator, ExecState
from dtypes import Name

def eq_ne(estate: ExecState, pyop: Callable[[Any, Any], bool]) -> None:
    a, b = estate.opop(2)
    match a, b:
        case (int() | float(), int() | float()):
            estate.opush(pyop(a, b))
        case (str() | Name(), str() | Name()):
            estate.opush(pyop(str(a), str(b)))
        case _:
            raise Tilted("typecheck")

def ge_etc(estate: ExecState, pyop: Callable[[Any, Any], bool]) -> None:
    a, b = estate.opop(2)
    match a, b:
        case (int() | float(), int() | float()):
            estate.opush(pyop(a, b))
        case (str(), str()):
            estate.opush(pyop(str(a), str(b)))
        case _:
            raise Tilted("typecheck")

@operator
def eq(estate: ExecState) -> None:
    eq_ne(estate, py_operator.eq)

@operator
def ge(estate: ExecState) -> None:
    ge_etc(estate, py_operator.ge)

@operator
def gt(estate: ExecState) -> None:
    ge_etc(estate, py_operator.gt)

@operator
def le(estate: ExecState) -> None:
    ge_etc(estate, py_operator.le)

@operator
def lt(estate: ExecState) -> None:
    ge_etc(estate, py_operator.lt)

@operator
def ne(estate: ExecState) -> None:
    eq_ne(estate, py_operator.ne)
