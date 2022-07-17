"""Built-in control operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import typecheck, Procedure


@operator("if")
def if_(estate: ExecState) -> None:
    b, proc_if = estate.opop(2)
    typecheck(bool, b)
    typecheck(Procedure, proc_if)
    if b:
        estate.run_proc(proc_if)

@operator
def ifelse(estate: ExecState) -> None:
    b, proc_if, proc_else = estate.opop(3)
    typecheck(bool, b)
    typecheck(Procedure, proc_if, proc_else)
    if b:
        estate.run_proc(proc_if)
    else:
        estate.run_proc(proc_else)
