"""Built-in graphics operators for stilted."""

from dtypes import from_py, typecheck, Number
from error import Tilted
from evaluate import operator, Engine

def has_current_point(engine: Engine) -> None:
    """There must be a current point, or raise nocurrentpoint."""
    if not engine.gctx.has_current_point():
        raise Tilted("nocurrentpoint")

@operator
def currentlinewidth(engine: Engine) -> None:
    engine.opush(from_py(engine.gctx.get_line_width()))

@operator
def currentpoint(engine: Engine) -> None:
    has_current_point(engine)
    x, y = engine.gctx.get_current_point()
    engine.opush(from_py(x), from_py(y))

@operator
def grestore(engine: Engine) -> None:
    if engine.gsaves:
        engine.gctx.restore()
        if engine.gsaves[-1].from_save:
            engine.gctx.save()
            gsx = engine.gsaves[-1]
        else:
            gsx = engine.gsaves.pop()
        gsx.restore_to_ctx(engine.gctx)

@operator
def grestoreall(engine: Engine) -> None:
    engine.grestoreall()

@operator
def gsave(engine: Engine) -> None:
    engine.gsave(from_save=False)

@operator
def lineto(engine: Engine) -> None:
    x, y = engine.opopn(2)
    typecheck(Number, x, y)
    has_current_point(engine)
    engine.gctx.line_to(x.value, y.value)

@operator
def moveto(engine: Engine) -> None:
    x, y = engine.opopn(2)
    typecheck(Number, x, y)
    engine.gctx.move_to(x.value, y.value)

@operator
def setlinewidth(engine: Engine) -> None:
    lw = engine.opop(Number)
    engine.gctx.set_line_width(lw.value)

@operator
def showpage(engine: Engine) -> None:
    engine.device.showpage()

@operator
def stroke(engine: Engine) -> None:
    engine.gctx.stroke()
