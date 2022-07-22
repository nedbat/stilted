"""Stack evaluation for stilted."""

from __future__ import annotations
from typing import Any, Iterable, Iterator

from error import Tilted
from lex import lexer
from dtypes import Float, Int, Name, Procedure

from estate import ExecState
import op_control
import op_math
import op_relational
import op_stack


def evaluate(text: str) -> ExecState:
    estate = ExecState.new()
    estate.estack.append(collect_objects(lexer.tokens(text)))

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
        case bool() | Int() | Float() | str():
            estate.opush(obj)

        case Name(True, name):
            estate.opush(obj)

        case Name(False, name):
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
