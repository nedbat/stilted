"""Built-in painting operators for Stilted."""

from evaluate import operator, Engine

@operator
def fill(engine: Engine) -> None:
    engine.gctx.fill()

@operator
def stroke(engine: Engine) -> None:
    engine.gctx.stroke()
