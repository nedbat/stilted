"""Built-in object model operators for stilted."""

from evaluate import operator, Engine
from dtypes import from_py, Name

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
