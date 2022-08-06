"""Built-in output operators for stilted."""

from evaluate import operator, Engine
from dtypes import Stringy

@operator("=")
def eq_(engine: Engine) -> None:
    o = engine.opop()
    engine.stdout.write(o.op_eq())
    engine.stdout.write("\n")

@operator("==")
def eqeq_(engine: Engine) -> None:
    o = engine.opop()
    engine.stdout.write(o.op_eqeq())
    engine.stdout.write("\n")

@operator("print")
def print_(engine: Engine) -> None:
    s = engine.opop(Stringy)
    engine.stdout.write(s.str_value)

@operator
def pstack(engine: Engine) -> None:
    for o in reversed(engine.ostack):
        engine.stdout.write(o.op_eqeq())
        engine.stdout.write("\n")

@operator
def stack(engine: Engine) -> None:
    for o in reversed(engine.ostack):
        engine.stdout.write(o.op_eq())
        engine.stdout.write("\n")
