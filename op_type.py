"""Built-in type/attribute/conversion operators for Stilted."""

import string

from error import Tilted
from evaluate import operator, Engine
from dtypes import (
    from_py, typecheck,
    Integer, Name, Number, Object, Real, String,
)
from lex import lexer
from util import rangecheck


@operator
def cvi(engine: Engine) -> None:
    obj = engine.opop()
    if isinstance(obj, String):
        obj = next(iter(lexer.tokens(obj.str_value)))
    match obj:
        case Integer():
            val: Object = obj
        case Real():
            val = from_py(int(obj.value))
        case _:
            print(f"{obj=}")
            raise Tilted("typecheck")
    engine.opush(val)

@operator
def cvlit(engine: Engine) -> None:
    engine.otop().literal = True

@operator
def cvn(engine: Engine) -> None:
    s = engine.opop(String)
    engine.opush(Name(literal=s.literal, value=s.str_value))

@operator
def cvr(engine: Engine) -> None:
    obj = engine.opop()
    match obj:
        case Integer() | Real() | String():
            try:
                val = float(obj.value)
            except ValueError:
                raise Tilted("undefinedresult")
            engine.opush(from_py(val))
        case _:
            raise Tilted("typecheck")

DIGITS = (string.digits + string.ascii_uppercase).encode("ascii")

@operator
def cvrs(engine: Engine) -> None:
    num, radix, s = engine.opopn(3)
    typecheck(Number, num)
    typecheck(Integer, radix)
    typecheck(String, s)
    radixv = radix.value
    rangecheck(2, radixv, 36)
    if radixv == 10:
        res = num.op_eq().encode("ascii")
    else:
        n = int(num.value) % 2**32
        res = []
        while True:
            n, digit = divmod(n, radixv)
            res.append(DIGITS[digit])
            if n == 0:
                break
        res = res[::-1]
    rangecheck(len(res), s.length)
    for i in range(len(res)):
        s[i] = res[i]
    engine.opush(s.new_sub(0, len(res)))

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
