"""Stack evaluation for stilted."""

from __future__ import annotations
from typing import Any, Iterable, Iterator

from error import Tilted
from lex import lexer
from dtypes import Name, Object, Operator, Procedure

from estate import ExecState

import op_array
import op_collections
import op_control
import op_dict
import op_math
import op_object
import op_output
import op_relational
import op_stack
import op_string
import op_vm


def evaluate(text: str, stdout=None) -> ExecState:
    estate = ExecState.new()
    estate.estack.append(collect_objects(lexer.tokens(text)))
    if stdout:
        estate.stdout = stdout

    while estate.estack:
        if callable(estate.estack[-1]):
            obj = estate.estack.pop()
        else:
            try:
                obj = next(estate.estack[-1])
            except StopIteration:
                estate.estack.pop()
                continue
        evaluate_one(obj, estate, direct=True)

    return estate


def collect_objects(tokens: Iterable[Any]) -> Iterator[Any]:
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


def evaluate_one(obj: Any, estate: ExecState, direct: bool=False) -> None:
    match obj:
        case Name(False, name):
            obj = estate.dstack_value(obj)
            if obj is None:
                raise Tilted(f"undefined: {name}")
            evaluate_one(obj, estate)

        case Procedure():
            if direct:
                estate.opush(obj)
            else:
                for subobj in obj.objs:
                    evaluate_one(subobj, estate)

        case Operator():
            obj.value(estate)

        case Object(literal=True):
            estate.opush(obj)

        case _ if callable(obj):
            obj(estate)

        case _:
            raise Exception(f"Buh? {obj!r}")
