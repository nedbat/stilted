"""Built-in control operators for stilted."""

import sys
from dataclasses import dataclass
from typing import Iterator, Tuple

from error import Tilted
from evaluate import operator, Engine, Exitable
from dtypes import (
    from_py, typecheck, typecheck_procedure,
    Array, Boolean, Dict, Integer, Name, Number, Object, String,
)
from util import rangecheck


@operator("exec")
def exec_(engine: Engine) -> None:
    obj = engine.opop()
    engine.exec(obj)

@operator("exit")
def exit_(engine: Engine) -> None:
    # Find the object with .exitable on the stack.
    while engine.estack and not hasattr(engine.estack[-1], "exitable"):
        engine.estack.pop()
    if engine.estack:
        # Pop the callable, it is done.
        engine.estack.pop()
    else:
        # No enclosing exitable operator, so "quit".
        engine.exec_name("quit")

@dataclass
class ForExec(Exitable):
    """Execstack item for implementing `for`."""
    control: float
    increment: float
    limit: float
    proc: Array

    def __call__(self, engine: Engine) -> None:
        if self.increment > 0:
            terminate = (self.control > self.limit)
        else:
            terminate = (self.control < self.limit)
        if not terminate:
            engine.opush(from_py(self.control))
            self.control += self.increment
            engine.estack.append(self)
            engine.exec(self.proc)

@operator("for")
def for_(engine: Engine) -> None:
    initial, increment, limit, proc = engine.opopn(4)
    typecheck(Number, initial, increment, limit)
    typecheck_procedure(proc)

    init_val = initial.value + type(increment.value)(0)
    engine.estack.append(ForExec(init_val, increment.value, limit.value, proc))

@dataclass
class ForallArrayExec(Exitable):
    """Execstack item for implementing `array {} forall`."""
    array_iter: Iterator[Object]
    proc: Array

    def __call__(self, engine: Engine) -> None:
        try:
            obj = next(self.array_iter)
        except StopIteration:
            return
        engine.opush(obj)
        engine.estack.append(self)
        engine.exec(self.proc)

@dataclass
class ForallDictExec(Exitable):
    """Execstack item for implementing `dict {} forall`."""
    items_iter: Iterator[Tuple[str, Object]]
    proc: Array

    def __call__(self, engine: Engine) -> None:
        try:
            k, v = next(self.items_iter)
        except StopIteration:
            return
        engine.opush(Name(True, k), v)
        engine.estack.append(self)
        engine.exec(self.proc)

@dataclass
class ForallStringExec(Exitable):
    """Execstack item for implementing `string {} forall`."""
    bytes_iter: Iterator[int]
    proc: Array

    def __call__(self, engine: Engine) -> None:
        try:
            b = next(self.bytes_iter)
        except StopIteration:
            return
        engine.opush(from_py(b))
        engine.estack.append(self)
        engine.exec(self.proc)

@operator
def forall(engine: Engine) -> None:
    o, proc = engine.opopn(2)
    typecheck(Array, proc)
    if proc.literal:
        raise Tilted("typecheck")

    match o:
        case Array():
            engine.estack.append(ForallArrayExec(iter(o), proc))

        case Dict():
            engine.estack.append(ForallDictExec(iter(o.value.items()), proc))

        case String():
            engine.estack.append(ForallStringExec(iter(o), proc))

        case _:
            raise Tilted("typecheck")

@operator("if")
def if_(engine: Engine) -> None:
    b, proc_if = engine.opopn(2)
    typecheck(Boolean, b)
    typecheck_procedure(proc_if)
    if b.value:
        engine.exec(proc_if)

@operator
def ifelse(engine: Engine) -> None:
    b, proc_if, proc_else = engine.opopn(3)
    typecheck(Boolean, b)
    typecheck_procedure(proc_if, proc_else)
    if b.value:
        engine.exec(proc_if)
    else:
        engine.exec(proc_else)

@dataclass
class LoopExec(Exitable):
    """Execstack item for implementing `loop`."""
    proc: Array

    def __call__(self, engine: Engine) -> None:
        engine.estack.append(self)
        engine.exec(self.proc)

@operator
def loop(engine: Engine) -> None:
    proc = engine.opop()
    typecheck_procedure(proc)
    engine.estack.append(LoopExec(proc))

@operator("quit")
def quit_(engine: Engine) -> None:
    sys.exit()

@dataclass
class RepeatExec(Exitable):
    count: int
    proc: Array

    def __call__(self, engine: Engine) -> None:
        if self.count > 0:
            self.count -= 1
            engine.estack.append(self)
            engine.exec(self.proc)

@operator
def repeat(engine: Engine) -> None:
    count, proc = engine.opopn(2)
    typecheck(Integer, count)
    typecheck_procedure(proc)
    countv = count.value
    rangecheck(0, countv)

    engine.estack.append(RepeatExec(countv, proc))

@dataclass
class StoppedExec:
    """Execstack item for `stopped`."""
    stoppable = True

    def __call__(self, engine: Engine) -> None:
        # If we get here, then no `stop` was executed.
        engine.opush(from_py(False))

@operator
def stop(engine: Engine) -> None:
    # Find the `stopped` object on the stack.
    while engine.estack and not hasattr(engine.estack[-1], "stoppable"):
        engine.estack.pop()
    if engine.estack:
        # `stopped` is done, and was stopped.
        engine.estack.pop()
        engine.opush(from_py(True))
    else:
        engine.exec_name("quit")

@operator
def stopped(engine: Engine) -> None:
    obj = engine.opop()
    engine.estack.append(StoppedExec())
    engine.exec(obj)
