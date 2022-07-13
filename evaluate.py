"""Stack evaluation for stilted."""

from typing import Any

from lex import lexer


def evaluate(text: str) -> list[Any]:
    stack: list[Any] = []
    for tok in lexer.tokens(text):
        match tok:
            case str() | int() | float():
                stack.append(tok)
            case _:
                raise Exception(f"Buh? {tok!r}")

    return stack
