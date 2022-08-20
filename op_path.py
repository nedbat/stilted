"""Built-in path construction operators for Stilted."""

from dataclasses import dataclass
from typing import Any, Iterator

import cairo

from cairo_util import has_current_point
from dtypes import from_py, typecheck_procedure, Array, Number
from evaluate import operator, Engine, Exitable
from util import deg_to_rad

@operator
def arc(engine: Engine) -> None:
    x, y, r, a1, a2 = engine.opopn(5, Number)
    engine.gctx.arc(x.value, y.value, r.value, deg_to_rad(a1.value), deg_to_rad(a2.value))

@operator
def arcn(engine: Engine) -> None:
    x, y, r, a1, a2 = engine.opopn(5, Number)
    engine.gctx.arc_negative(x.value, y.value, r.value, deg_to_rad(a1.value), deg_to_rad(a2.value))

@operator
def clip(engine: Engine) -> None:
    engine.gctx.set_fill_rule(cairo.FillRule.WINDING)
    engine.gctx.clip_preserve()

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
    x1, y1, x2, y2, x3, y3 = engine.opopn(6, Number)
    engine.gctx.curve_to(x1.value, y1.value, x2.value, y2.value, x3.value, y3.value)

@operator
def eoclip(engine: Engine) -> None:
    engine.gctx.set_fill_rule(cairo.FillRule.EVEN_ODD)
    engine.gctx.clip_preserve()

@operator
def initclip(engine: Engine) -> None:
    engine.gctx.reset_clip()

@operator
def lineto(engine: Engine) -> None:
    x, y = engine.opopn(2, Number)
    has_current_point(engine)
    engine.gctx.line_to(x.value, y.value)

@operator
def moveto(engine: Engine) -> None:
    x, y = engine.opopn(2, Number)
    engine.gctx.move_to(x.value, y.value)

@operator
def newpath(engine: Engine) -> None:
    engine.gctx.new_path()

@dataclass
class PathforallExec(Exitable):
    """Execstack item for implementing `pathforall`."""
    segment_iter: Iterator[Any]
    procs: list[Array]

    def __call__(self, engine: Engine) -> None:
        try:
            kind, nums = next(self.segment_iter)
        except StopIteration:
            return
        # Cairo always puts a moveto after a closepath, but PostScript does not.
        # If we have a closepath, swallow the moveto after it.
        if kind == 3:
            next(self.segment_iter)
        engine.opush(*map(from_py, nums))
        engine.estack.append(self)
        engine.exec(self.procs[kind])

@operator
def pathforall(engine: Engine) -> None:
    procs = engine.opopn(4)
    typecheck_procedure(*procs)
    engine.estack.append(PathforallExec(iter(engine.gctx.copy_path()), procs))

@operator
def rcurveto(engine: Engine) -> None:
    dx1, dy1, dx2, dy2, dx3, dy3 = engine.opopn(6, Number)
    has_current_point(engine)
    engine.gctx.rel_curve_to(dx1.value, dy1.value, dx2.value, dy2.value, dx3.value, dy3.value)

@operator
def rlineto(engine: Engine) -> None:
    dx, dy = engine.opopn(2, Number)
    has_current_point(engine)
    engine.gctx.rel_line_to(dx.value, dy.value)

@operator
def rmoveto(engine: Engine) -> None:
    dx, dy = engine.opopn(2, Number)
    has_current_point(engine)
    engine.gctx.rel_move_to(dx.value, dy.value)
