"""Built-in relational operators for stilted."""

import operator as py_operator
from typing import Any, Callable

from error import Tilted
from estate import operator, ExecState
from dtypes import from_py, Boolean, Integer, Name, Real, String


def eq_ne(estate: ExecState, pyop: Callable[[Any, Any], bool]) -> None:
    a, b = estate.opopn(2)
    match a, b:
        case (Integer() | Real(), Integer() | Real()):
            estate.opush(from_py(pyop(a.value, b.value)))
        case (String() | Name(), String() | Name()):
            estate.opush(from_py(pyop(a.value, b.value)))
        case _:
            raise Tilted("typecheck")


def ge_etc(estate: ExecState, pyop: Callable[[Any, Any], bool]) -> None:
    a, b = estate.opopn(2)
    match a, b:
        case (Integer() | Real(), Integer() | Real()):
            estate.opush(from_py(pyop(a.value, b.value)))
        case (String(), String()):
            estate.opush(from_py(pyop(a.value, b.value)))
        case _:
            raise Tilted("typecheck")


def bool_op(
    estate: ExecState,
    py_bool_op: Callable[[Any, Any], bool],
    py_int_op: Callable[[Any, Any], int],
) -> None:
    a, b = estate.opopn(2)
    match a, b:
        case (Boolean(), Boolean()):
            estate.opush(from_py(py_bool_op(a.value, b.value)))
        case (Integer(), Integer()):
            estate.opush(from_py(py_int_op(a.value, b.value)))
        case _:
            raise Tilted("typecheck")


@operator("and")
def and_(estate: ExecState) -> None:
    bool_op(estate, lambda a, b: a and b, py_operator.and_)

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

@operator("not")
def not_(estate: ExecState) -> None:
    a = estate.opop()
    match a:
        case Boolean():
            estate.opush(from_py(not a.value))
        case Integer():
            estate.opush(from_py(-(a.value + 1)))
        case _:
            raise Tilted("typecheck")

@operator("or")
def or_(estate: ExecState) -> None:
    bool_op(estate, lambda a, b: a or b, py_operator.or_)

@operator
def xor(estate: ExecState) -> None:
    bool_op(estate, lambda a, b: a != b, py_operator.xor)
