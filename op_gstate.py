"""Built-in graphics state operators for stilted."""

import colorsys

import cairo

from dtypes import clamp, from_py, typecheck, Number
from error import Tilted
from evaluate import operator, Engine

@operator
def currentcmykcolor(engine: Engine) -> None:
    r, g, b, _ = engine.gctx.get_source().get_rgba()

@operator
def currentgray(engine: Engine) -> None:
    r, g, b, _ = engine.gctx.get_source().get_rgba()
    gray = 0.3 * r + 0.59 * g + 0.11 * b
    engine.opush(from_py(gray))

@operator
def currenthsbcolor(engine: Engine) -> None:
    r, g, b, _ = engine.gctx.get_source().get_rgba()
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    engine.opush(from_py(h), from_py(s), from_py(v))

@operator
def currentlinecap(engine: Engine) -> None:
    lc = engine.gctx.get_line_cap()
    engine.opush(from_py(int(lc)))

@operator
def currentlinejoin(engine: Engine) -> None:
    lc = engine.gctx.get_line_join()
    engine.opush(from_py(int(lc)))

@operator
def currentlinewidth(engine: Engine) -> None:
    engine.opush(from_py(engine.gctx.get_line_width()))

@operator
def currentmiterlimit(engine: Engine) -> None:
    engine.opush(from_py(engine.gctx.get_miter_limit()))

@operator
def currentrgbcolor(engine: Engine) -> None:
    r, g, b, _ = engine.gctx.get_source().get_rgba()
    engine.opush(from_py(r), from_py(g), from_py(b))

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
def setgray(engine: Engine) -> None:
    gray = engine.opop(Number)
    gv = clamp(0.0, gray.value, 1.0)
    engine.gctx.set_source_rgb(gv, gv, gv)

@operator
def sethsbcolor(engine: Engine) -> None:
    h, s, v = engine.opopn(3)
    typecheck(Number, h, s, v)
    hv = clamp(0.0, h.value, 1.0)
    sv = clamp(0.0, s.value, 1.0)
    vv = clamp(0.0, v.value, 1.0)
    r, g, b = colorsys.hsv_to_rgb(hv, sv, vv)
    engine.gctx.set_source_rgb(r, g, b)

@operator
def setlinecap(engine: Engine) -> None:
    lc = engine.opop(Number).value
    if lc not in {0, 1, 2}:
        raise Tilted("rangecheck")
    engine.gctx.set_line_cap(cairo.LineCap(lc))

@operator
def setlinejoin(engine: Engine) -> None:
    lj = engine.opop(Number).value
    if lj not in {0, 1, 2}:
        raise Tilted("rangecheck")
    engine.gctx.set_line_join(cairo.LineJoin(lj))

@operator
def setlinewidth(engine: Engine) -> None:
    lw = engine.opop(Number).value
    engine.gctx.set_line_width(lw)

@operator
def setmiterlimit(engine: Engine) -> None:
    ml = engine.opop(Number).value
    engine.gctx.set_miter_limit(ml)

@operator
def setrgbcolor(engine: Engine) -> None:
    r, g, b = engine.opopn(3)
    typecheck(Number, r, g, b)
    rv = clamp(0.0, r.value, 1.0)
    gv = clamp(0.0, g.value, 1.0)
    bv = clamp(0.0, b.value, 1.0)
    engine.gctx.set_source_rgb(rv, gv, bv)

@operator
def showpage(engine: Engine) -> None:
    engine.device.showpage()
