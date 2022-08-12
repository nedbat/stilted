"""Built-in path construction operators for Stilted."""

from dtypes import from_py, typecheck, Number
from error import Tilted
from evaluate import operator, Engine
from util import deg_to_rad

def has_current_point(engine: Engine) -> None:
    """There must be a current point, or raise nocurrentpoint."""
    if not engine.gctx.has_current_point():
        raise Tilted("nocurrentpoint")

@operator
def arc(engine: Engine) -> None:
    x, y, r, a1, a2 = engine.opopn(5)
    typecheck(Number, x, y, r, a1, a2)
    engine.gctx.arc(x.value, y.value, r.value, deg_to_rad(a1.value), deg_to_rad(a2.value))

@operator
def arcn(engine: Engine) -> None:
    x, y, r, a1, a2 = engine.opopn(5)
    typecheck(Number, x, y, r, a1, a2)
    engine.gctx.arc_negative(x.value, y.value, r.value, deg_to_rad(a1.value), deg_to_rad(a2.value))

@operator
def clip(engine: Engine) -> None:
    engine.gctx.clip()

@operator
def closepath(engine: Engine) -> None:
    engine.gctx.close_path()

@operator
def currentpoint(engine: Engine) -> None:
    has_current_point(engine)
    x, y = engine.gctx.get_current_point()
    engine.opush(from_py(x), from_py(y))

@operator
def curveto(engine: Engine) -> None:
    x1, y1, x2, y2, x3, y3 = engine.opopn(6)
    typecheck(Number, x1, y1, x2, y2, x3, y3)
    engine.gctx.curve_to(x1.value, y1.value, x2.value, y2.value, x3.value, y3.value)

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
def newpath(engine: Engine) -> None:
    engine.gctx.new_path()

@operator
def rcurveto(engine: Engine) -> None:
    dx1, dy1, dx2, dy2, dx3, dy3 = engine.opopn(6)
    typecheck(Number, dx1, dy1, dx2, dy2, dx3, dy3)
    has_current_point(engine)
    engine.gctx.rel_curve_to(dx1.value, dy1.value, dx2.value, dy2.value, dx3.value, dy3.value)

@operator
def rlineto(engine: Engine) -> None:
    dx, dy = engine.opopn(2)
    typecheck(Number, dx, dy)
    has_current_point(engine)
    engine.gctx.rel_line_to(dx.value, dy.value)

@operator
def rmoveto(engine: Engine) -> None:
    dx, dy = engine.opopn(2)
    typecheck(Number, dx, dy)
    has_current_point(engine)
    engine.gctx.rel_move_to(dx.value, dy.value)
