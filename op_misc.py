"""Built-in miscellaneous operators for Stilted."""

import time

from dtypes import from_py, Array, Name, Operator
from evaluate import operator, Engine

@operator
def bind(engine: Engine) -> None:

    def bind_proc(proc: Array) -> None:
        """Recursive function to replace executable names with operators."""
        for i, elt in enumerate(proc):
            match elt:
                case Array():
                    bind_proc(elt)

                case Name(literal=False):
                    val = engine.dstack_value(elt)
                    if isinstance(val, Operator):
                        proc[i] = val

    proc = engine.opop(Array)
    bind_proc(proc)
    engine.opush(proc)

@operator
def usertime(engine: Engine) -> None:
    engine.opush(from_py(int(time.process_time() * 1000)))
