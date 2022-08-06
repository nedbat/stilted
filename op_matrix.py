"""Built-in matrix and coordinate operators for stilted."""

import math

import cairo

from dtypes import from_py, typecheck, Array, Real, Integer, Number
from error import Tilted
from estate import operator, ExecState

def pop_matrix(estate: ExecState) -> Array:
    """Pop a matrix from the stack."""
    arr = estate.opop(Array)
    if len(arr) != 6:
        raise Tilted("rangecheck")
    return arr

def matrix_to_array(mtx: cairo.Matrix, arr: Array):
    """Assign mtx into arr."""
    lmtx = list(mtx) # type: ignore
    for i in range(6):
        arr[i] = from_py(lmtx[i])

def deg_to_rad(degrees: float) -> float:
    """Convert degrees to radians."""
    return math.pi * degrees / 180

@operator
def currentmatrix(estate: ExecState) -> None:
    arr = pop_matrix(estate)
    matrix_to_array(estate.gctx.get_matrix(), arr)
    estate.opush(arr)

@operator
def identmatrix(estate: ExecState) -> None:
    arr = pop_matrix(estate)
    matrix_to_array(cairo.Matrix(), arr)
    estate.opush(arr)

@operator
def matrix(estate: ExecState) -> None:
    arr = estate.new_array(n=6)
    matrix_to_array(cairo.Matrix(), arr)
    estate.opush(arr)

@operator
def rotate(estate: ExecState) -> None:
    match estate.otop():
        case Array():
            arr = pop_matrix(estate)
            ang = estate.opop(Number)
            matrix_to_array(cairo.Matrix.init_rotate(deg_to_rad(ang.value)), arr)
            estate.opush(arr)

        case Integer() | Real():
            ang = estate.opop(Number)
            estate.gctx.rotate(deg_to_rad(ang.value))

        case _:
            raise Tilted("typecheck")

@operator
def scale(estate: ExecState) -> None:
    match estate.otop():
        case Array():
            arr = pop_matrix(estate)
            sx, sy = estate.opopn(2)
            typecheck(Number, sx, sy)
            matrix_to_array(cairo.Matrix(xx=sx.value, yy=sy.value), arr)
            estate.opush(arr)

        case Integer() | Real():
            sx, sy = estate.opopn(2)
            typecheck(Number, sx, sy)
            estate.gctx.scale(sx.value, sy.value)

        case _:
            raise Tilted("typecheck")

@operator
def translate(estate: ExecState) -> None:
    match estate.otop():
        case Array():
            arr = pop_matrix(estate)
            tx, ty = estate.opopn(2)
            typecheck(Number, tx, ty)
            matrix_to_array(cairo.Matrix(x0=tx.value, y0=ty.value), arr)
            estate.opush(arr)

        case Integer() | Real():
            tx, ty = estate.opopn(2)
            typecheck(Number, tx, ty)
            estate.gctx.translate(tx.value, ty.value)

        case _:
            raise Tilted("typecheck")
