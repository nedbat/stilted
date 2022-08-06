"""Built-in matrix and coordinate operators for stilted."""

from dtypes import from_py, typecheck, Array, Real, Integer, Number
from error import Tilted
from estate import operator, ExecState

def pop_matrix(estate: ExecState) -> Array:
    """Pop a matrix from the stack."""
    arr = estate.opop(Array)
    if len(arr) != 6:
        raise Tilted("rangecheck")
    return arr

@operator
def currentmatrix(estate: ExecState) -> None:
    arr = pop_matrix(estate)
    mtx = list(estate.gctx.get_matrix())
    for i in range(6):
        arr[i] = from_py(mtx[i])
    estate.opush(arr)

@operator
def identmatrix(estate: ExecState) -> None:
    arr = pop_matrix(estate)
    mtx = [1, 0, 0, 1, 0, 0]
    for i in range(6):
        arr[i] = from_py(mtx[i])
    estate.opush(arr)

@operator
def matrix(estate: ExecState) -> None:
    arr = list(map(from_py, [1, 0, 0, 1, 0, 0]))
    estate.opush(estate.new_array(value=arr))

@operator
def translate(estate: ExecState) -> None:
    match estate.otop():
        case Array():
            raise Tilted("unregistered")

        case Integer() | Real():
            tx, ty = estate.opopn(2)
            typecheck(Number, tx, ty)
            estate.gctx.translate(tx.value, ty.value)

        case _:
            raise Tilted("typecheck")
