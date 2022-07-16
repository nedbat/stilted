"""Stack evaluation for stilted."""

from __future__ import annotations
from typing import Any, Iterable

from error import Tilted
from lex import lexer
from dtypes import Name, Procedure

from estate import ExecState
import op_math
import op_relational
import op_stack


def evaluate(text: str) -> ExecState:
    estate = ExecState.new()
    tokens = lexer.tokens(text)
    for obj in collect_objects(tokens):
        evaluate_one(obj, estate, direct=True)

    return estate


def collect_objects(tokens: Iterable[Any]) -> Iterable[Any]:
    pstack: list[Any] = []
    for obj in tokens:
        match obj:
            case Name("{", literal=False):
                pstack.append([])

            case Name("}", literal=False):
                if not pstack:
                    raise Tilted("syntaxerror")
                proc = Procedure(pstack.pop())
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
        case str() | int() | float():
            estate.opush(obj)

        case Name(name, literal=True):
            estate.opush(obj)

        case Name(name, literal=False):
            try:
                obj = estate.dstack[name]
            except KeyError:
                raise Tilted("undefined")
            evaluate_one(obj, estate)

        case Procedure():
            if direct:
                estate.opush(obj)
            else:
                for subobj in obj.objs:
                    evaluate_one(subobj, estate)

        case _ if callable(obj):
            obj(estate)

        case _:
            raise Exception(f"Buh? {obj!r}")
