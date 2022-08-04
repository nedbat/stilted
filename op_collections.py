"""Built-in collections operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import (
    from_py, rangecheck, typecheck,
    Array, Dict, Integer, Name, String, Stringy,
)

@operator
def forall(estate: ExecState) -> None:
    o, proc = estate.opopn(2)
    typecheck(Array, proc)
    if proc.literal:
        raise Tilted("typecheck")

    match o:
        case Array():
            def _do_forall_array(estate: ExecState) -> None:
                array_iter, proc = estate.estack.pop()
                try:
                    obj = next(array_iter)
                except StopIteration:
                    return
                estate.opush(obj)
                estate.estack.extend([[array_iter, proc], _do_forall_array])
                estate.run_proc(proc)

            _do_forall_array.exitable = True  # type: ignore
            estate.estack.extend([[iter(o), proc], _do_forall_array])

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
            estate.estack.extend([[iter(o), proc], _do_forall_string])

        case _:
            raise Tilted("typecheck")

@operator
def get(estate: ExecState) -> None:
    obj, ind = estate.opopn(2)
    match obj:
        case Array():
            typecheck(Integer, ind)
            rangecheck(0, ind.value, len(obj.value)-1)
            elt = obj[ind.value]
            estate.opush(elt)

        case Dict():
            typecheck(Stringy, ind)
            try:
                obj = obj[ind.str_value]
            except KeyError:
                raise Tilted(f"undefined: {ind.value}")
            estate.opush(obj)

        case String():
            typecheck(Integer, ind)
            rangecheck(0, ind.value, obj.length - 1)
            byte = obj[ind.value]
            estate.opush(from_py(byte))

        case _:
            raise Tilted(f"typecheck: got {type(obj)}")

@operator
def getinterval(estate: ExecState) -> None:
    obj, ind, count = estate.opopn(3)
    typecheck(Integer, ind, count)
    match obj:
        case Array() | String():
            estate.opush(obj.new_sub(ind.value, count.value))

        case _:
            raise Tilted(f"typecheck: got {type(obj)}")

@operator
def length(estate: ExecState) -> None:
    o = estate.opop()
    match o:
        case Array() | String():
            estate.opush(from_py(len(o)))

        case Dict() | Name():
            estate.opush(from_py(len(o.value)))

        case _:
            raise Tilted(f"typecheck: got {type(o)}")

@operator
def put(estate: ExecState) -> None:
    obj, ind, elt = estate.opopn(3)
    match obj:
        case Array():
            typecheck(Integer, ind)
            rangecheck(0, ind.value, len(obj.value)-1)
            estate.prep_for_change(obj)
            obj[ind.value] = elt

        case Dict():
            typecheck(Stringy, ind)
            estate.prep_for_change(obj)
            obj[ind.str_value] = elt

        case String():
            typecheck(Integer, ind, elt)
            rangecheck(0, elt.value, 255)
            rangecheck(0, ind.value, obj.length - 1)
            obj[ind.value] = elt.value

        case _:
            raise Tilted(f"typecheck: got {type(obj)}")

@operator
def putinterval(estate: ExecState) -> None:
    obj1, ind, obj2 = estate.opopn(3)
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
            raise Tilted(f"typecheck: got {type(obj1)}")
