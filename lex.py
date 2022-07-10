"""Lexical analysis for stilted."""

import re
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Tuple


@dataclass
class Token:
    """A token that we want."""
    rx: str
    kind: str
    converter: Callable[[str], Any] = lambda text: text

    def pattern(self):
        return f"(?P<{self.kind}>{self.rx})"

@dataclass
class Skip:
    """Characters that can be discarded."""
    rx: str
    kind: None = None

    def pattern(self):
        return f"({self.rx})"

class Lexer:
    """
    A lexical analyzer.

    Initialize with a bunch of Token/Skip instances.
    """
    def __init__(self, *tokens) -> None:
        self.rx = "(?m)" + "|".join(t.pattern() for t in tokens)
        self.converters = {t.kind: t.converter for t in tokens if t.kind}

    def tokens(self, text: str) -> Iterable[Tuple[str, Any]]:
        """
        Yield (kind, value) pairs for the tokens in `text`.
        """
        for match in re.finditer(self.rx, text):
            if kind := match.lastgroup:
                converter = self.converters[kind]
                yield (kind, converter(match[0]))


def convert_string(text: str) -> str:
    """
    A converter for raw string text to the string value we want.
    """
    assert text[0] == "("
    assert text[-1] == ")"

    def do_escape(match):
        if match[0][1] in "01234567":
            return chr(int(match[0][1:], 8))
        else:
            match match[0]:
                case r"\n":
                    return "\n"
                case r"\t":
                    return "\t"
                case "\\\n":
                    return ""
                case _:
                    return match[0][1]

    return re.sub(r"(?s)\\[0-7]{1,3}|\\.", do_escape, text[1:-1])

lexer = Lexer(
    Token(r"\((?:\\\[0-7]{1,3}|\\.|\\\n|.|\n)*?\)", "string", convert_string),
    Token(r"[-+]?\d*(\d\.|\.\d)\d*", "float", float),
    Token(r"[-+]?\d+", "int", int),
    Skip(r"%.*$"),
    Skip(r"\s+"),
    Token(r".", "error"),
)
