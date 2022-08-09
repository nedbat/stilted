"""Built-in object model operators for stilted."""

from error import Tilted
from evaluate import operator, Engine
from dtypes import from_py, Integer, Name, Real, String

@operator
def cvi(engine: Engine) -> None:
    obj = engine.opop()
    match obj:
        case Integer() | Real() | String():
            try:
                val = int(float(obj.value))
            except ValueError:
                raise Tilted("undefinedresult")
            engine.opush(from_py(val))
        case _:
            raise Tilted("typecheck")

@operator
def cvlit(engine: Engine) -> None:
    engine.otop().literal = True

@operator
def cvx(engine: Engine) -> None:
    engine.otop().literal = False

@operator("type")
def type_(engine: Engine) -> None:
    obj = engine.opop()
    engine.opush(Name(literal=False, value=obj.typename + "type"))

@operator
def xcheck(engine: Engine) -> None:
    obj = engine.opop()
    engine.opush(from_py(not obj.literal))
