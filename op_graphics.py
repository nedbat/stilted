"""Built-in graphics operators for stilted."""

from dtypes import from_py, typecheck, Array, Real, Integer, Number
from error import Tilted
from estate import operator, ExecState

def has_current_point(estate: ExecState) -> None:
    """There must be a current point, or raise nocurrentpoint."""
    if not estate.gctx.has_current_point():
        raise Tilted("nocurrentpoint")

@operator
def currentlinewidth(estate: ExecState) -> None:
    estate.opush(from_py(estate.gctx.get_line_width()))

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
def currentpoint(estate: ExecState) -> None:
    has_current_point(estate)
    x, y = estate.gctx.get_current_point()
    estate.opush(from_py(x), from_py(y))

@operator
def grestore(estate: ExecState) -> None:
    if estate.gsaves:
        estate.gctx.restore()
        if estate.gsaves[-1].from_save:
            estate.gctx.save()
            gsx = estate.gsaves[-1]
        else:
            gsx = estate.gsaves.pop()
        gsx.restore_to_ctx(estate.gctx)

@operator
def grestoreall(estate: ExecState) -> None:
    estate.grestoreall()

@operator
def gsave(estate: ExecState) -> None:
    estate.gsave(from_save=False)

@operator
def lineto(estate: ExecState) -> None:
    x, y = estate.opopn(2)
    typecheck(Number, x, y)
    has_current_point(estate)
    estate.gctx.line_to(x.value, y.value)

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
def moveto(estate: ExecState) -> None:
    x, y = estate.opopn(2)
    typecheck(Number, x, y)
    estate.gctx.move_to(x.value, y.value)

@operator
def setlinewidth(estate: ExecState) -> None:
    lw = estate.opop(Number)
    estate.gctx.set_line_width(lw.value)

@operator
def showpage(estate: ExecState) -> None:
    estate.device.showpage()

@operator
def stroke(estate: ExecState) -> None:
    estate.gctx.stroke()

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
