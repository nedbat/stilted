"""Built-in collections operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import from_py, typecheck, Dict, Integer, Name, Procedure, String, Stringy

@operator
def forall(estate: ExecState) -> None:
    o, proc = estate.opopn(2)
    typecheck(Procedure, proc)
    match o:
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

        case _:
            raise Tilted("typecheck")


@operator
def get(estate: ExecState) -> None:
    d, k = estate.opopn(2)
    typecheck(Dict, d)
    typecheck(Stringy, k)
    try:
        obj = d.value[k.value]
    except KeyError:
        raise Tilted(f"undefined: {k.value}")
    estate.opush(obj)

@operator
def length(estate: ExecState) -> None:
    d = estate.opop()
    typecheck(Dict, d)
    estate.opush(from_py(len(d.value)))

@operator
def put(estate: ExecState) -> None:
    d, k, o = estate.opopn(3)
    typecheck(Dict, d)
    typecheck(Stringy, k)
    estate.prep_for_change(d)
    d.value[k.value] = o
