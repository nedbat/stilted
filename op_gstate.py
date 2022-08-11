"""Built-in graphics state operators for stilted."""

from dtypes import clamp, from_py, typecheck, Number
from evaluate import operator, Engine

@operator
def currentgray(engine: Engine) -> None:
    r, g, b, _ = engine.gctx.get_source().get_rgba()
    gray = 0.3 * r + 0.59 * g + 0.11 * b
    engine.opush(from_py(gray))

@operator
def currentlinewidth(engine: Engine) -> None:
    engine.opush(from_py(engine.gctx.get_line_width()))

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
def setlinewidth(engine: Engine) -> None:
    lw = engine.opop(Number)
    engine.gctx.set_line_width(lw.value)

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
