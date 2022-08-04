"""Built-in control operators for stilted."""

import sys
from dataclasses import dataclass
from typing import Iterator, Tuple

from error import Tilted
from estate import operator, ExecState
from dtypes import (
    from_py, rangecheck, typecheck,
    Array, Boolean, Dict, Integer, Name, Number, Object, String,
)


def typecheck_procedure(*objs):
    """Type-check that all `objs` are procedures (executable arrays)."""
    for obj in objs:
        typecheck(Array, obj)
        if obj.literal:
            raise Tilted("typecheck")

@dataclass
class Exitable:
    """An item on the execstack that can be `exit`ed."""
    exitable = True

@operator("exit")
def exit_(estate: ExecState) -> None:
    # Find the object with .exitable on the stack.
    while estate.estack and not hasattr(estate.estack[-1], "exitable"):
        estate.estack.pop()
    if estate.estack:
        # Pop the callable, it is done.
        estate.estack.pop()
    else:
        # No enclosing exitable operator, so "quit".
        estate.run_name("quit")

@dataclass
class ForExec(Exitable):
    """Execstack item for implementing `for`."""
    control: float
    increment: float
    limit: float
    proc: Array

    def __call__(self, estate: ExecState) -> None:
        if self.increment > 0:
            terminate = (self.control > self.limit)
        else:
            terminate = (self.control < self.limit)
        if not terminate:
            estate.opush(from_py(self.control))
            self.control += self.increment
            estate.estack.append(self)
            estate.run_proc(self.proc)

@operator("for")
def for_(estate: ExecState) -> None:
    initial, increment, limit, proc = estate.opopn(4)
    typecheck(Number, initial, increment, limit)
    typecheck_procedure(proc)

    init_val = initial.value + type(increment.value)(0)
    estate.estack.append(ForExec(init_val, increment.value, limit.value, proc))

@dataclass
class ForallArrayExec(Exitable):
    """Execstack item for implementing `array {} forall`."""
    array_iter: Iterator[Object]
    proc: Array

    def __call__(self, estate: ExecState) -> None:
        try:
            obj = next(self.array_iter)
        except StopIteration:
            return
        estate.opush(obj)
        estate.estack.append(self)
        estate.run_proc(self.proc)

@dataclass
class ForallDictExec(Exitable):
    """Execstack item for implementing `dict {} forall`."""
    items_iter: Iterator[Tuple[str, Object]]
    proc: Array

    def __call__(self, estate: ExecState) -> None:
        try:
            k, v = next(self.items_iter)
        except StopIteration:
            return
        estate.opush(Name(True, k), v)
        estate.estack.append(self)
        estate.run_proc(self.proc)

@dataclass
class ForallStringExec(Exitable):
    """Execstack item for implementing `string {} forall`."""
    bytes_iter: Iterator[int]
    proc: Array

    def __call__(self, estate: ExecState) -> None:
        try:
            b = next(self.bytes_iter)
        except StopIteration:
            return
        estate.opush(from_py(b))
        estate.estack.append(self)
        estate.run_proc(self.proc)

@operator
def forall(estate: ExecState) -> None:
    o, proc = estate.opopn(2)
    typecheck(Array, proc)
    if proc.literal:
        raise Tilted("typecheck")

    match o:
        case Array():
            estate.estack.append(ForallArrayExec(iter(o), proc))

        case Dict():
            estate.estack.append(ForallDictExec(iter(o.value.items()), proc))

        case String():
            estate.estack.append(ForallStringExec(iter(o), proc))

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

@dataclass
class LoopExec(Exitable):
    """Execstack item for implementing `loop`."""
    proc: Array

    def __call__(self, estate: ExecState) -> None:
        estate.estack.append(self)
        estate.run_proc(self.proc)

@operator
def loop(estate: ExecState) -> None:
    proc = estate.opop()
    typecheck_procedure(proc)
    estate.estack.append(LoopExec(proc))

@operator("quit")
def quit_(estate: ExecState) -> None:
    sys.exit()

@dataclass
class RepeatExec(Exitable):
    count: int
    proc: Array

    def __call__(self, estate: ExecState) -> None:
        if self.count > 0:
            self.count -= 1
            estate.estack.append(self)
            estate.run_proc(self.proc)

@operator
def repeat(estate: ExecState) -> None:
    count, proc = estate.opopn(2)
    typecheck(Integer, count)
    typecheck_procedure(proc)
    countv = count.value
    rangecheck(0, countv)

    estate.estack.append(RepeatExec(countv, proc))

@dataclass
class StoppedExec:
    """Exectack item for `stopped`."""
    stoppable = True

    def __call__(self, estate: ExecState) -> None:
        # If we get here, then no `stop` was executed.
        estate.opush(from_py(False))

@operator
def stop(estate: ExecState) -> None:
    # Find the `stopped` object on the stack.
    while estate.estack and not hasattr(estate.estack[-1], "stoppable"):
        estate.estack.pop()
    if estate.estack:
        # `stopped` is done, and was stopped.
        estate.estack.pop()
        estate.opush(from_py(True))
    else:
        estate.run_name("quit")

@operator
def stopped(estate: ExecState) -> None:
    proc = estate.opop()
    typecheck_procedure(proc)
    estate.estack.append(StoppedExec())
    estate.run_proc(proc)
