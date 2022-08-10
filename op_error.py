"""Built-in error operators for Stilted."""

from typing import cast

from error import StiltedError
from evaluate import operator, Engine
from dtypes import from_py, Boolean, Name


@operator(".error")
def dot_error_(engine: Engine) -> None:
    serror = engine.builtin_dict("$error")
    serror["newerror"] = from_py(True)
    serror["errorname"] = engine.opop()
    serror["command"] = engine.opop()
    engine.exec_name("stop")

@operator
def handleerror(engine: Engine) -> None:
    serror = engine.builtin_dict("$error")
    if cast(Boolean, serror["newerror"]).value:
        serror["newerror"] = from_py(False)
        errorname = cast(Name, serror["errorname"])
        command = serror["command"]
        print(f"Error: {errorname.str_value} in {command.op_eqeq()}")
        print(f"Operand stack ({len(engine.ostack)}):")
        engine.pstack(engine.ostack)

@operator(".pyraise")
def pyraise_(engine: Engine) -> None:
    name = engine.opop()
    raise StiltedError(name.str_value)
