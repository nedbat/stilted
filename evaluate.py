"""Stack evaluation for stilted."""

from __future__ import annotations
from typing import Any

from error import Tilted
from lex import lexer
from dtypes import Name

from estate import ExecState
import op_math
import op_stack

def evaluate(text: str) -> ExecState:
    estate = ExecState.new()
    for tok in lexer.tokens(text):
        evaluate_one(tok, estate)

    return estate

def evaluate_one(obj: Any, estate: ExecState) -> None:
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

        case _ if callable(obj):
            obj(estate)

        case _:
            raise Exception(f"Buh? {obj!r}")
