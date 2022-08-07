"""Built-in collections operators for stilted."""

from error import Tilted
from evaluate import operator, Engine
from dtypes import (
    from_py, rangecheck, typecheck,
    Array, Dict, Integer, Name, String, Stringy,
)

@operator
def get(engine: Engine) -> None:
    obj, ind = engine.opopn(2)
    match obj:
        case Array():
            typecheck(Integer, ind)
            rangecheck(0, ind.value, len(obj.value)-1)
            elt = obj[ind.value]
            engine.opush(elt)

        case Dict():
            typecheck(Stringy, ind)
            try:
                obj = obj[ind.str_value]
            except KeyError:
                raise Tilted("undefined", f"{ind.value}")
            engine.opush(obj)

        case String():
            typecheck(Integer, ind)
            rangecheck(0, ind.value, obj.length - 1)
            byte = obj[ind.value]
            engine.opush(from_py(byte))

        case _:
            raise Tilted("typecheck", f"got {type(obj)}")

@operator
def getinterval(engine: Engine) -> None:
    obj, ind, count = engine.opopn(3)
    typecheck(Integer, ind, count)
    match obj:
        case Array() | String():
            engine.opush(obj.new_sub(ind.value, count.value))

        case _:
            raise Tilted("typecheck", f"got {type(obj)}")

@operator
def length(engine: Engine) -> None:
    o = engine.opop()
    match o:
        case Array() | String():
            engine.opush(from_py(len(o)))

        case Dict() | Name():
            engine.opush(from_py(len(o.value)))

        case _:
            raise Tilted("typecheck", f"got {type(o)}")

@operator
def put(engine: Engine) -> None:
    obj, ind, elt = engine.opopn(3)
    match obj:
        case Array():
            typecheck(Integer, ind)
            rangecheck(0, ind.value, len(obj.value)-1)
            engine.prep_for_change(obj)
            obj[ind.value] = elt

        case Dict():
            typecheck(Stringy, ind)
            engine.prep_for_change(obj)
            obj[ind.str_value] = elt

        case String():
            typecheck(Integer, ind, elt)
            rangecheck(0, elt.value, 255)
            rangecheck(0, ind.value, obj.length - 1)
            obj[ind.value] = elt.value

        case _:
            raise Tilted("typecheck", f"got {type(obj)}")

@operator
def putinterval(engine: Engine) -> None:
    obj1, ind, obj2 = engine.opopn(3)
    typecheck(Integer, ind)
    match obj1, obj2:
        case (Array(), Array()) | (String(), String()):
            if not (0 <= ind.value <= obj1.length):
                raise Tilted("rangecheck")
            if not (ind.value + obj2.length <= obj1.length):
                raise Tilted("rangecheck")
            for i in range(obj2.length):
                obj1[ind.value + i] = obj2[i]

        case _:
            raise Tilted("typecheck", f"got {type(obj1)}")
