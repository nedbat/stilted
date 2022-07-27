"""Built-in collections operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import (
    from_py, typecheck,
    Array, Dict, Integer, Name, Procedure, String, Stringy,
)

@operator
def forall(estate: ExecState) -> None:
    o, proc = estate.opopn(2)
    typecheck(Procedure, proc)
    match o:
        case Array():
            def _do_forall_array(estate: ExecState) -> None:
                aiter, proc = estate.estack.pop()
                try:
                    obj = next(aiter)
                except StopIteration:
                    return
                estate.opush(obj)
                estate.estack.extend([[aiter, proc], _do_forall_array])
                estate.run_proc(proc)

            _do_forall_array.exitable = True  # type: ignore
            estate.estack.extend([[iter(o.value), proc], _do_forall_array])

        case Dict():
            def _do_forall_dict(estate: ExecState) -> None:
                diter, proc = estate.estack.pop()
                try:
                    k, v = next(diter)
                except StopIteration:
                    return
                estate.opush(Name(True, k), v)
                estate.estack.extend([[diter, proc], _do_forall_dict])
                estate.run_proc(proc)

            _do_forall_dict.exitable = True  # type: ignore
            estate.estack.extend([[iter(o.value.items()), proc], _do_forall_dict])

        case String():
            def _do_forall_string(estate: ExecState) -> None:
                biter, proc = estate.estack.pop()
                try:
                    b = next(biter)
                except StopIteration:
                    return
                estate.opush(from_py(b))
                estate.estack.extend([[biter, proc], _do_forall_string])
                estate.run_proc(proc)

            _do_forall_string.exitable = True  # type: ignore
            estate.estack.extend([[iter(o.value), proc], _do_forall_string])

        case _:
            raise Tilted("typecheck")

@operator
def get(estate: ExecState) -> None:
    obj, ind = estate.opopn(2)
    match obj:
        case Array():
            typecheck(Integer, ind)
            if ind.value < 0:
                raise Tilted("rangecheck")
            try:
                elt = obj[ind.value]
            except IndexError:
                raise Tilted("rangecheck")
            estate.opush(elt)

        case Dict():
            typecheck(Stringy, ind)
            try:
                obj = obj[ind.value]
            except KeyError:
                raise Tilted(f"undefined: {ind.value}")
            estate.opush(obj)

        case String():
            typecheck(Integer, ind)
            if ind.value < 0:
                raise Tilted("rangecheck")
            try:
                byte = obj[ind.value]
            except IndexError:
                raise Tilted("rangecheck")
            estate.opush(from_py(byte))

        case _:
            raise Tilted(f"typecheck: got {type(obj)}")

@operator
def getinterval(estate: ExecState) -> None:
    obj, ind, count = estate.opopn(3)
    typecheck(Integer, ind, count)
    match obj:
        case String():
            estate.opush(obj.new_sub(ind.value, count.value))

        case _:
            raise Tilted(f"typecheck: got {type(obj)}")

@operator
def length(estate: ExecState) -> None:
    o = estate.opop()
    match o:
        case Array() | Dict() | Name() | String():
            estate.opush(from_py(len(o.value)))
        case _:
            raise Tilted(f"typecheck: got {type(o)}")

@operator
def put(estate: ExecState) -> None:
    obj, ind, elt = estate.opopn(3)
    match obj:
        case Array():
            typecheck(Integer, ind)
            if not (0 <= ind.value < len(obj.value)):
                raise Tilted("rangecheck")
            estate.prep_for_change(obj)
            obj[ind.value] = elt

        case Dict():
            typecheck(Stringy, ind)
            estate.prep_for_change(obj)
            obj[ind.value] = elt

        case String():
            typecheck(Integer, ind, elt)
            if not (0 <= elt.value < 256):
                raise Tilted("rangecheck")
            try:
                obj[ind.value] = elt.value
            except IndexError:
                raise Tilted("rangecheck")

        case _:
            raise Tilted(f"typecheck: got {type(obj)}")

@operator
def putinterval(estate: ExecState) -> None:
    obj, ind, obj2 = estate.opopn(3)
    typecheck(Integer, ind)
    match obj:
        case String():
            typecheck(String, obj2)
            if not (0 <= ind.value <= obj.length):
                raise Tilted("rangecheck")
            if not (ind.value + obj2.length <= obj.length):
                raise Tilted("rangecheck")
            for i in range(obj2.length):
                obj[ind.value + i] = obj2[i]

        case _:
            raise Tilted(f"typecheck: got {type(obj)}")
