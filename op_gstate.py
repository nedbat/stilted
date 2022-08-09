"""Built-in graphics state operators for stilted."""

from dtypes import from_py, Number
from evaluate import operator, Engine

@operator
def currentlinewidth(engine: Engine) -> None:
    engine.opush(from_py(engine.gctx.get_line_width()))

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
def setlinewidth(engine: Engine) -> None:
    lw = engine.opop(Number)
    engine.gctx.set_line_width(lw.value)

@operator
def showpage(engine: Engine) -> None:
    engine.device.showpage()
