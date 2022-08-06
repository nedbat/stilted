"""Built-in relational operators for stilted."""

import operator as py_operator
from typing import Any, Callable

from error import Tilted
from evaluate import operator, Engine
from dtypes import from_py, Boolean, Integer, Name, Real, String


def eq_ne(engine: Engine, pyop: Callable[[Any, Any], bool]) -> None:
    a, b = engine.opopn(2)
    match a, b:
        case (Integer() | Real(), Integer() | Real()):
            engine.opush(from_py(pyop(a.value, b.value)))
        case (String() | Name(), String() | Name()):
            engine.opush(from_py(pyop(a.str_value, b.str_value)))
        case _:
            raise Tilted("typecheck")


def ge_etc(engine: Engine, pyop: Callable[[Any, Any], bool]) -> None:
    a, b = engine.opopn(2)
    match a, b:
        case (Integer() | Real(), Integer() | Real()):
            engine.opush(from_py(pyop(a.value, b.value)))
        case (String(), String()):
            engine.opush(from_py(pyop(a.str_value, b.str_value)))
        case _:
            raise Tilted("typecheck")


def bool_op(
    engine: Engine,
    py_bool_op: Callable[[Any, Any], bool],
    py_int_op: Callable[[Any, Any], int],
) -> None:
    a, b = engine.opopn(2)
    match a, b:
        case (Boolean(), Boolean()):
            engine.opush(from_py(py_bool_op(a.value, b.value)))
        case (Integer(), Integer()):
            engine.opush(from_py(py_int_op(a.value, b.value)))
        case _:
            raise Tilted("typecheck")


@operator("and")
def and_(engine: Engine) -> None:
    bool_op(engine, lambda a, b: a and b, py_operator.and_)

@operator
def eq(engine: Engine) -> None:
    eq_ne(engine, py_operator.eq)

@operator
def ge(engine: Engine) -> None:
    ge_etc(engine, py_operator.ge)

@operator
def gt(engine: Engine) -> None:
    ge_etc(engine, py_operator.gt)

@operator
def le(engine: Engine) -> None:
    ge_etc(engine, py_operator.le)

@operator
def lt(engine: Engine) -> None:
    ge_etc(engine, py_operator.lt)

@operator
def ne(engine: Engine) -> None:
    eq_ne(engine, py_operator.ne)

@operator("not")
def not_(engine: Engine) -> None:
    a = engine.opop()
    match a:
        case Boolean():
            engine.opush(from_py(not a.value))
        case Integer():
            engine.opush(from_py(-(a.value + 1)))
        case _:
            raise Tilted("typecheck")

@operator("or")
def or_(engine: Engine) -> None:
    bool_op(engine, lambda a, b: a or b, py_operator.or_)

@operator
def xor(engine: Engine) -> None:
    bool_op(engine, lambda a, b: a != b, py_operator.xor)
