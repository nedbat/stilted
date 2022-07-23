"""Built-in output operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import Name, String

@operator("=")
def eq_(estate: ExecState) -> None:
    o = estate.opop(1)[0]
    estate.stdout.write(o.op_eq())
    estate.stdout.write("\n")

@operator("==")
def eqeq_(estate: ExecState) -> None:
    o = estate.opop(1)[0]
    estate.stdout.write(o.op_eqeq())
    estate.stdout.write("\n")

@operator("print")
def print_(estate: ExecState) -> None:
    s = estate.opop(1)[0]
    match s:
        case String() | Name():
            estate.stdout.write(s.value)
        case _:
            raise Tilted("typecheck")

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
