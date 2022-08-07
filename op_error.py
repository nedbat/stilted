"""Built-in error operators for stilted."""

from error import FinalTilt
from evaluate import operator, Engine
from dtypes import from_py


@operator
def _stdhandleerror(engine: Engine) -> None:
    serror = engine.builtin_dict("$error")
    serror["newerror"] = from_py(True)
    serror["errorname"] = errorname = engine.opop()
    serror["command"] = engine.opop()
    print(f"!!! {errorname.str_value}")
    raise FinalTilt()
