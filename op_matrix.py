"""Built-in matrix and coordinate operators for stilted."""

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
def translate(estate: ExecState) -> None:
    match estate.otop():
        case Array():
            arr = estate.opop()
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
