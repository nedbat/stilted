"""Built-in control operators for stilted."""

import sys

from error import Tilted
from estate import operator, ExecState
from dtypes import (
    from_py, rangecheck, typecheck,
    Array, Boolean, Dict, Integer, Name, Number, String,
)


def typecheck_procedure(*objs):
    """Type-check that all `objs` are procedures (executable arrays)."""
    for obj in objs:
        typecheck(Array, obj)
        if obj.literal:
            raise Tilted("typecheck")

@operator("exit")
def exit_(estate: ExecState) -> None:
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
    initial, increment, limit, proc = estate.opopn(4)
    typecheck(Number, initial, increment, limit)
    typecheck_procedure(proc)

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

@operator
def forall(estate: ExecState) -> None:
    o, proc = estate.opopn(2)
    typecheck(Array, proc)
    if proc.literal:
        raise Tilted("typecheck")

    match o:
        case Array():
            def _do_forall_array(estate: ExecState) -> None:
                array_iter, proc = estate.estack.pop()
                try:
                    obj = next(array_iter)
                except StopIteration:
                    return
                estate.opush(obj)
                estate.estack.extend([[array_iter, proc], _do_forall_array])
                estate.run_proc(proc)

            _do_forall_array.exitable = True  # type: ignore
            estate.estack.extend([[iter(o), proc], _do_forall_array])

        case Dict():
            def _do_forall_dict(estate: ExecState) -> None:
                diter, proc = estate.estack.pop()
                try:
                    k, v = next(diter)
                except StopIteration:
                    return
                estate.opush(Name(True, k), v)
                estate.estack.extend([[diter, proc], _do_forall_dict])
                estate.run_proc(proc)

            _do_forall_dict.exitable = True  # type: ignore
            estate.estack.extend([[iter(o.value.items()), proc], _do_forall_dict])

        case String():
            def _do_forall_string(estate: ExecState) -> None:
                biter, proc = estate.estack.pop()
                try:
                    b = next(biter)
                except StopIteration:
                    return
                estate.opush(from_py(b))
                estate.estack.extend([[biter, proc], _do_forall_string])
                estate.run_proc(proc)

            _do_forall_string.exitable = True  # type: ignore
            estate.estack.extend([[iter(o), proc], _do_forall_string])

        case _:
            raise Tilted("typecheck")

@operator("if")
def if_(estate: ExecState) -> None:
    b, proc_if = estate.opopn(2)
    typecheck(Boolean, b)
    typecheck_procedure(proc_if)
    if b.value:
        estate.run_proc(proc_if)

@operator
def ifelse(estate: ExecState) -> None:
    b, proc_if, proc_else = estate.opopn(3)
    typecheck(Boolean, b)
    typecheck_procedure(proc_if, proc_else)
    if b.value:
        estate.run_proc(proc_if)
    else:
        estate.run_proc(proc_else)

@operator
def loop(estate: ExecState) -> None:
    proc = estate.opop()
    typecheck_procedure(proc)

    def _do_loop(estate: ExecState) -> None:
        proc = estate.estack.pop()
        estate.estack.extend([proc, _do_loop])
        estate.run_proc(proc)

    _do_loop.exitable = True     # type: ignore
    estate.estack.extend([proc, _do_loop])

@operator("quit")
def quit_(estate: ExecState) -> None:
    sys.exit()

@operator
def repeat(estate: ExecState) -> None:
    n, proc = estate.opopn(2)
    typecheck(Integer, n)
    typecheck_procedure(proc)
    nv = n.value
    rangecheck(0, nv)

    def _do_repeat(estate: ExecState) -> None:
        nv, proc = estate.estack.pop()
        if nv > 0:
            estate.estack.extend([[nv - 1, proc], _do_repeat])
            estate.run_proc(proc)

    _do_repeat.exitable = True     # type: ignore
    estate.estack.extend([[nv, proc], _do_repeat])
