"""Built-in error operators for stilted."""

from error import FinalTilt
from evaluate import operator, Engine
from dtypes import from_py


@operator
def _stdhandleerror(engine: Engine) -> None:
    serror = engine.builtin_dict("$error")
    serror["newerror"] = from_py(True)
    serror["errorname"] = errorname = engine.opop()
    serror["command"] = command = engine.opop()
    print(f"Error: {errorname.str_value} in {command.op_eqeq()}")
    print(f"Operand stack ({len(engine.ostack)}):")
    engine.pstack(engine.ostack)
    raise FinalTilt()
