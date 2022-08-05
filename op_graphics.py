"""Built-in graphics operators for stilted."""

from dtypes import from_py, typecheck, Number
from error import Tilted
from estate import operator, ExecState

def has_current_point(estate: ExecState) -> None:
    """There must be a current point, or raise nocurrentpoint."""
    if not estate.gctx.has_current_point():
        raise Tilted("nocurrentpoint")

@operator
def currentlinewidth(estate: ExecState) -> None:
    estate.opush(from_py(estate.gctx.get_line_width()))

@operator
def currentpoint(estate: ExecState) -> None:
    has_current_point(estate)
    x, y = estate.gctx.get_current_point()
    estate.opush(from_py(x), from_py(y))

@operator
def lineto(estate: ExecState) -> None:
    x, y = estate.opopn(2)
    typecheck(Number, x, y)
    has_current_point(estate)
    estate.gctx.line_to(x.value, y.value)

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
