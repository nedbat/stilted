"""Lexical analysis for stilted."""

import re
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Tuple


@dataclass
class Token:
    """A token that we want."""

    rx: str
    converter: Callable[[str], Any] = lambda text: text
    keep: bool = True

    def pattern(self):
        return f"(?P<{self.kind}>{self.rx})"


@dataclass
class Skip:
    """Characters that can be discarded."""

    rx: str
    keep: bool = False

    def pattern(self):
        return f"({self.rx})"


class Lexer:
    """
    A lexical analyzer.

    Initialize with a bunch of Token/Skip instances.
    """

    def __init__(self, *tokens) -> None:
        rxes = []
        self.converters = {}
        for i, t in enumerate(tokens):
            if t.keep:
                group_name = f"g{i}"
                rxes.append(f"(?P<{group_name}>{t.rx})")
                self.converters[group_name] = t.converter
            else:
                rxes.append(f"({t.rx})")
        self.rx = "(?m)" + "|".join(rxes)

    def tokens(self, text: str) -> Iterable[Tuple[str, Any]]:
        """
        Yield (kind, value) pairs for the tokens in `text`.
        """
        for match in re.finditer(self.rx, text):
            if group_name := match.lastgroup:
                converter = self.converters[group_name]
                yield converter(match[0])


def convert_string(text: str) -> str:
    """
    A converter for raw string text to the string value we want.
    """
    assert text[0] == "("
    assert text[-1] == ")"

    def do_escape(match):
        esc_text = match[0]
        if esc_text[1] in "01234567":
            return chr(int(esc_text[1:], 8))
        else:
            match esc_text:
                case r"\n":
                    return "\n"
                case r"\t":
                    return "\t"
                case "\\\n":
                    return ""
                case _:
                    return esc_text[1]

    return re.sub(r"(?s)\\[0-7]{1,3}|\\.", do_escape, text[1:-1])

def error(text: str):
    raise Exception(f"Lexical error: {text!r}")

lexer = Lexer(
    Token(r"\((?:\\\[0-7]{1,3}|\\.|\\\n|.|\n)*?\)", convert_string),
    Token(r"[-+]?\d*(\d\.|\.\d)\d*", float),
    Token(r"[-+]?\d+", int),
    Skip(r"%.*$"),
    Skip(r"\s+"),
    Token(r".", error),
)
