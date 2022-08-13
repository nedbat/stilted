"""Built-in painting operators for Stilted."""

import cairo

from evaluate import operator, Engine

@operator
def eofill(engine: Engine) -> None:
    engine.gctx.set_fill_rule(cairo.FillRule.EVEN_ODD)
    engine.gctx.fill()

@operator
def fill(engine: Engine) -> None:
    engine.gctx.set_fill_rule(cairo.FillRule.WINDING)
    engine.gctx.fill()

@operator
def stroke(engine: Engine) -> None:
    engine.gctx.stroke()
