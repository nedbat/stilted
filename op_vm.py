"""Built-in VM operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import typecheck, Save

@operator
def restore(estate: ExecState) -> None:
    s = estate.opop(Save)
    if not s.is_valid:
        raise Tilted("invalidrestore")
    assert s in estate.sstack
    for save in reversed(estate.sstack):
        for obj in save.changed_objs:
            if obj.values[-1][0] is save:
                obj.values.pop()
        estate.sstack.pop()
        save.is_valid = False
        if save is s:
            break

@operator
def save(estate: ExecState) -> None:
    estate.opush(estate.new_save())
