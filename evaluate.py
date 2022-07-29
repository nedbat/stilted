"""Stack evaluation for stilted."""

from __future__ import annotations
from typing import Any, Iterable, Iterator

from error import Tilted
from lex import lexer
from dtypes import Name, Object, Operator, Procedure

from estate import ExecState

# Imported but not used, assert them to quiet the linter
import op_array; assert op_array
import op_collections; assert op_collections
import op_control; assert op_control
import op_dict; assert op_dict
import op_math; assert op_math
import op_object; assert op_object
import op_output; assert op_output
import op_relational; assert op_relational
import op_stack; assert op_stack
import op_string; assert op_string
import op_vm; assert op_vm


class Engine:
    def __init__(self):
        self.estate = ExecState.new()

    def add_text(self, text: str) -> None:
        self.estate.estack.append(collect_objects(lexer.tokens(text)))

    def run(self) -> None:
        """Run the engine until it stops."""
        while self.estate.estack:
            if callable(self.estate.estack[-1]):
                obj = self.estate.estack.pop()
            else:
                try:
                    obj = next(self.estate.estack[-1])
                except StopIteration:
                    self.estate.estack.pop()
                    continue
            self.evaluate_one(obj, direct=True)

    def evaluate_one(self, obj: Any, direct: bool=False) -> None:
        match obj:
            case Name(False, name):
                obj = self.estate.dstack_value(obj)
                if obj is None:
                    raise Tilted(f"undefined: {name}")
                self.evaluate_one(obj)

            case Procedure():
                if direct:
                    self.estate.opush(obj)
                else:
                    for subobj in obj.objs:
                        self.evaluate_one(subobj)

            case Operator():
                obj.value(self.estate)

            case Object(literal=True):
                self.estate.opush(obj)

            case _ if callable(obj):
                obj(self.estate)

            case _:
                raise Exception(f"Buh? {obj!r}")


def evaluate(text: str, stdout=None) -> ExecState:
    """A simple helper to execute text."""
    engine = Engine()
    if stdout:
        engine.estate.stdout = stdout
    engine.add_text(text)
    engine.run()
    return engine.estate


def collect_objects(tokens: Iterable[Any]) -> Iterator[Any]:
    """Assemble tokens into objects."""
    pstack: list[Any] = []
    for obj in tokens:
        match obj:
            case Name(False, "{"):
                pstack.append([])

            case Name(False, "}"):
                if not pstack:
                    raise Tilted("syntaxerror")
                proc = Procedure(False, pstack.pop())
                if pstack:
                    pstack[-1].append(proc)
                else:
                    yield proc

            case _:
                if pstack:
                    pstack[-1].append(obj)
                else:
                    yield obj

    if pstack:
        raise Tilted("syntaxerror")
