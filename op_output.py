"""Built-in output operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import Name, Stringy

@operator("=")
def eq_(estate: ExecState) -> None:
    o = estate.opop()
    estate.stdout.write(o.op_eq())
    estate.stdout.write("\n")

@operator("==")
def eqeq_(estate: ExecState) -> None:
    o = estate.opop()
    estate.stdout.write(o.op_eqeq())
    estate.stdout.write("\n")

@operator("print")
def print_(estate: ExecState) -> None:
    s = estate.opop(Stringy)
    estate.stdout.write(s.value)

@operator
def pstack(estate: ExecState) -> None:
    for o in reversed(estate.ostack):
        estate.stdout.write(o.op_eqeq())
        estate.stdout.write("\n")

@operator
def stack(estate: ExecState) -> None:
    for o in reversed(estate.ostack):
        estate.stdout.write(o.op_eq())
        estate.stdout.write("\n")
