"""Stack evaluation for stilted."""

from __future__ import annotations
from typing import Any, Iterable, Iterator

from error import Tilted
from lex import lexer
from dtypes import Array, Name, Object, Operator

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
    """Stilted execution engine."""

    def __init__(self, stdout=None) -> None:
        self.estate = ExecState.new()
        if stdout is not None:
            self.estate.stdout = stdout

    def add_text(self, text: str) -> None:
        """Consume text as Stilted tokens, and add for execution."""
        self.estate.estack.append(self.collect_objects(lexer.tokens(text)))

    def collect_objects(self, tokens: Iterable[Any]) -> Iterator[Any]:
        """Assemble tokens into objects."""
        pstack: list[Any] = []
        for obj in tokens:
            match obj:
                case Name(False, "{"):
                    pstack.append([])

                case Name(False, "}"):
                    if not pstack:
                        raise Tilted("syntaxerror")
                    proc = self.estate.new_array(value=pstack.pop())
                    proc.literal = False
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

    def run(self) -> None:
        """Run the engine until it stops."""
        while self.estate.estack:
            if callable(self.estate.estack[-1]):
                func = self.estate.estack.pop()
                func(self.estate)
            else:
                try:
                    obj = next(self.estate.estack[-1])
                except StopIteration:
                    self.estate.estack.pop()
                    continue
                self._evaluate_one(obj, direct=True)

    def _evaluate_one(self, obj: Object, direct: bool=False) -> None:
        """Evaluate one Stilted Object."""
        match obj:
            case Name(literal=False, value=name):
                looked_up = self.estate.dstack_value(obj)
                if looked_up is None:
                    raise Tilted(f"undefined: {name}")
                self._evaluate_one(looked_up)

            case Array(literal=False):
                if direct:
                    self.estate.opush(obj)
                else:
                    for subobj in obj.value:
                        self._evaluate_one(subobj)

            case Operator():
                obj.value(self.estate)

            case Object(literal=True):
                self.estate.opush(obj)

            case _:
                raise Exception(f"Buh? {obj!r}")


def evaluate(text: str, stdout=None) -> ExecState:
    """A simple helper to execute text."""
    engine = Engine(stdout=stdout)
    engine.add_text(text)
    engine.run()
    return engine.estate
