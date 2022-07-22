"""Built-in control operators for stilted."""

import sys

from error import Tilted
from estate import operator, ExecState
from dtypes import from_py, typecheck, Int, Number, Procedure


@operator
def exit(estate: ExecState) -> None:
    # Find the function with .exitable on the stack.
    while estate.estack and not hasattr(estate.estack[-1], "exitable"):
        estate.estack.pop()
    if estate.estack:
        # Pop the function and its bundle of arguments.
        estate.estack.pop()
        estate.estack.pop()
    else:
        # No enclosing exitable operator, so "quit".
        estate.run_name("quit")

@operator("for")
def for_(estate: ExecState) -> None:
    initial, increment, limit, proc = estate.opop(4)
    typecheck(Number, initial, increment, limit)
    typecheck(Procedure, proc)

    def _do_for(estate: ExecState) -> None:
        control, increment, limit, proc = estate.estack.pop()
        terminate = (control > limit) if (increment > 0) else (control < limit)
        if not terminate:
            estate.opush(from_py(control))
            control += increment
            estate.estack.extend([[control, increment, limit, proc], _do_for])
            estate.run_proc(proc)

    _do_for.exitable = True     # type: ignore
    init_val = initial.value + type(increment.value)(0)
    estate.estack.extend([[init_val, increment.value, limit.value, proc], _do_for])

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

@operator
def quit(estate: ExecState) -> None:
    sys.exit()

@operator
def repeat(estate: ExecState) -> None:
    n, proc = estate.opop(2)
    typecheck(Procedure, proc)
    typecheck(Int, n)
    nv = n.value
    if nv < 0:
        raise Tilted("rangecheck")

    def _do_repeat(estate: ExecState) -> None:
        nv, proc = estate.estack.pop()
        if nv > 0:
            estate.estack.extend([[nv - 1, proc], _do_repeat])
            estate.run_proc(proc)

    _do_repeat.exitable = True     # type: ignore
    estate.estack.extend([[nv, proc], _do_repeat])
