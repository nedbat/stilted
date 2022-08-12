"""Built-in matrix and coordinate operators for stilted."""

import cairo

from dtypes import from_py, typecheck, Array, Real, Integer, Number
from error import Tilted
from evaluate import operator, Engine
from util import deg_to_rad

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

def transform_help(engine: Engine, *, invert: bool, distance: bool) -> None:
    """Code common to the four xxtransform operators."""
    match engine.otop():
        case Array():
            mtx = array_to_matrix(pop_matrix(engine))

        case Integer() | Real():
            mtx = engine.gctx.get_matrix()

        case _:
            raise Tilted("typecheck")

    if invert:
        try:
            mtx.invert()
        except cairo.Error:
            raise Tilted("undefinedresult")

    fn = mtx.transform_distance if distance else mtx.transform_point
    x, y = engine.opopn(2)
    typecheck(Number, x, y)
    x, y = fn(x.value, y.value)
    engine.opush(from_py(x), from_py(y))


@operator
def concat(engine: Engine) -> None:
    mtx = array_to_matrix(pop_matrix(engine))
    mtx = mtx.multiply(engine.gctx.get_matrix())
    engine.gctx.set_matrix(mtx)

@operator
def concatmatrix(engine: Engine) -> None:
    arr3 = pop_matrix(engine)
    mtx2 = array_to_matrix(pop_matrix(engine))
    mtx1 = array_to_matrix(pop_matrix(engine))
    mtx3 = mtx1.multiply(mtx2)
    matrix_to_array(mtx3, arr3)
    engine.opush(arr3)

@operator
def currentmatrix(engine: Engine) -> None:
    arr = pop_matrix(engine)
    matrix_to_array(engine.gctx.get_matrix(), arr)
    engine.opush(arr)

@operator
def defaultmatrix(engine: Engine) -> None:
    arr = pop_matrix(engine)
    matrix_to_array(engine.device.default_matrix, arr)
    engine.opush(arr)

@operator
def dtransform(engine: Engine) -> None:
    transform_help(engine, invert=False, distance=True)

@operator
def identmatrix(engine: Engine) -> None:
    arr = pop_matrix(engine)
    matrix_to_array(cairo.Matrix(), arr)
    engine.opush(arr)

@operator
def idtransform(engine: Engine) -> None:
    transform_help(engine, invert=True, distance=True)

@operator
def initmatrix(engine: Engine) -> None:
    engine.gctx.set_matrix(engine.device.default_matrix)

@operator
def invertmatrix(engine: Engine) -> None:
    arr2 = pop_matrix(engine)
    arr1 = pop_matrix(engine)
    mtx1 = array_to_matrix(arr1)
    try:
        mtx1.invert()
    except cairo.Error:
        raise Tilted("undefinedresult")
    matrix_to_array(mtx1, arr2)
    engine.opush(arr2)

@operator
def itransform(engine: Engine) -> None:
    transform_help(engine, invert=True, distance=False)

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
    transform_help(engine, invert=False, distance=False)

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
