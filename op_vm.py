"""Built-in VM operators for stilted."""

from error import Tilted
from estate import operator, ExecState
from dtypes import Save, SaveableObject

@operator
def restore(estate: ExecState) -> None:
    s = estate.opop(Save)
    if not s.is_valid:
        raise Tilted("invalidrestore")
    assert s in estate.sstack
    for save_obj in reversed(estate.sstack):
        for obj in save_obj.changed_objs:
            if obj.values[-1][0] is save_obj:
                obj.values.pop()
        estate.sstack.pop()
        save_obj.is_valid = False
        if save_obj is s:
            break

    # Check the ostack and dstack for things newer than the savepoint.
    for stack in [estate.ostack, estate.dstack]:
        for o in stack:     # type: ignore
            if isinstance(o, SaveableObject):
                if o.storage.values[0][0].serial >= s.serial:
                    raise Tilted("invalidrestore")

@operator
def save(estate: ExecState) -> None:
    estate.opush(estate.new_save())
