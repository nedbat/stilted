"""Built-in matrix and coordinate operators for stilted."""

import math

import cairo

from dtypes import from_py, typecheck, Array, Real, Integer, Number
from error import Tilted
from evaluate import operator, Engine

def pop_matrix(engine: Engine) -> Array:
    """Pop a matrix from the stack."""
    arr = engine.opop(Array)
    if len(arr) != 6:
        raise Tilted("rangecheck")
    return arr

def matrix_to_array(mtx: cairo.Matrix, arr: Array):
    """Assign mtx into arr."""
    lmtx = list(mtx) # type: ignore
    for i in range(6):
        arr[i] = from_py(lmtx[i])

def array_to_matrix(arr) -> cairo.Matrix:
    """Convert an Array into a Matrix."""
    return cairo.Matrix(*map(lambda o: o.value, arr))

def deg_to_rad(degrees: float) -> float:
    """Convert degrees to radians."""
    return math.pi * degrees / 180

@operator
def currentmatrix(engine: Engine) -> None:
    arr = pop_matrix(engine)
    matrix_to_array(engine.gctx.get_matrix(), arr)
    engine.opush(arr)

@operator
def identmatrix(engine: Engine) -> None:
    arr = pop_matrix(engine)
    matrix_to_array(cairo.Matrix(), arr)
    engine.opush(arr)

@operator
def matrix(engine: Engine) -> None:
    arr = engine.new_array(n=6)
    matrix_to_array(cairo.Matrix(), arr)
    engine.opush(arr)

@operator
def rotate(engine: Engine) -> None:
    match engine.otop():
        case Array():
            arr = pop_matrix(engine)
            ang = engine.opop(Number)
            matrix_to_array(cairo.Matrix.init_rotate(deg_to_rad(ang.value)), arr)
            engine.opush(arr)

        case Integer() | Real():
            ang = engine.opop(Number)
            engine.gctx.rotate(deg_to_rad(ang.value))

        case _:
            raise Tilted("typecheck")

@operator
def scale(engine: Engine) -> None:
    match engine.otop():
        case Array():
            arr = pop_matrix(engine)
            sx, sy = engine.opopn(2)
            typecheck(Number, sx, sy)
            matrix_to_array(cairo.Matrix(xx=sx.value, yy=sy.value), arr)
            engine.opush(arr)

        case Integer() | Real():
            sx, sy = engine.opopn(2)
            typecheck(Number, sx, sy)
            engine.gctx.scale(sx.value, sy.value)

        case _:
            raise Tilted("typecheck")

@operator
def setmatrix(engine: Engine) -> None:
    arr = pop_matrix(engine)
    engine.gctx.set_matrix(array_to_matrix(arr))

@operator
def transform(engine: Engine) -> None:
    match engine.otop():
        case Array():
            arr = pop_matrix(engine)
            x, y = engine.opopn(2)
            typecheck(Number, x, y)
            mtx = array_to_matrix(arr)
            x, y = mtx.transform_point(x.value, y.value)
            engine.opush(from_py(x), from_py(y))

        case Integer() | Real():
            x, y = engine.opopn(2)
            typecheck(Number, x, y)
            x, y = engine.gctx.get_matrix().transform_point(x.value, y.value)
            engine.opush(from_py(x), from_py(y))

        case _:
            raise Tilted("typecheck")

@operator
def translate(engine: Engine) -> None:
    match engine.otop():
        case Array():
            arr = pop_matrix(engine)
            tx, ty = engine.opopn(2)
            typecheck(Number, tx, ty)
            matrix_to_array(cairo.Matrix(x0=tx.value, y0=ty.value), arr)
            engine.opush(arr)

        case Integer() | Real():
            tx, ty = engine.opopn(2)
            typecheck(Number, tx, ty)
            engine.gctx.translate(tx.value, ty.value)

        case _:
            raise Tilted("typecheck")
