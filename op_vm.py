"""Built-in VM operators for stilted."""

from error import Tilted
from evaluate import operator, Engine
from dtypes import Save, SaveableObject

@operator
def restore(engine: Engine) -> None:
    s = engine.opop(Save)
    if not s.is_valid:
        raise Tilted("invalidrestore")
    assert s in engine.sstack
    for save_obj in reversed(engine.sstack):
        for obj in save_obj.changed_objs:
            if obj.values[-1][0] is save_obj:
                obj.values.pop()
        engine.sstack.pop()
        save_obj.is_valid = False
        if save_obj is s:
            break

    # Check the ostack and dstack for things newer than the savepoint.
    for stack in [engine.ostack, engine.dstack]:
        for o in stack:     # type: ignore
            if isinstance(o, SaveableObject):
                if o.storage.values[0][0].serial >= s.serial:
                    raise Tilted("invalidrestore")

    # Roll back the gstack also.
    engine.grestoreall()

@operator
def save(engine: Engine) -> None:
    engine.opush(engine.new_save())
    engine.gsave(from_save=True)
