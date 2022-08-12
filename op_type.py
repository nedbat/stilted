"""Built-in type/attribute/conversion operators for Stilted."""

from error import Tilted
from evaluate import operator, Engine
from dtypes import from_py, rangecheck, typecheck, Integer, Name, Real, String

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
def cvn(engine: Engine) -> None:
    s = engine.opop(String)
    engine.opush(Name(literal=s.literal, value=s.str_value))

@operator
def cvs(engine: Engine) -> None:
    obj, s = engine.opopn(2)
    typecheck(String, s)
    eqs = obj.op_eq().encode("iso8859-1")
    rangecheck(len(eqs), s.length)
    for i in range(len(eqs)):
        s[i] = eqs[i]
    engine.opush(s.new_sub(0, len(eqs)))

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
