"""Stack evaluation for stilted."""

from __future__ import annotations
from typing import Any

from lex import lexer, Name

from estate import ExecState
import op_stack

def evaluate(text: str) -> ExecState:
    estate = ExecState.new()
    for tok in lexer.tokens(text):
        evaluate_one(tok, estate)

    return estate

def evaluate_one(obj: Any, estate: ExecState) -> None:
    match obj:
        case str() | int() | float():
            estate.ostack.append(obj)

        case Name(name, literal=True):
            estate.ostack.append(obj)

        case Name(name, literal=False):
            evaluate_one(estate.dstack[name], estate)

        case _ if callable(obj):
            obj(estate)

        case _:
            raise Exception(f"Buh? {obj!r}")
