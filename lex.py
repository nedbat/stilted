"""

(string(withparens))
123
123.23
2#010101
Names 123ABC $$^&
/Literalnames
%comments

"""


import re


class Lexer:
    def __init__(self, *tokens):
        self.rx = "(?m)" + "|".join(tokens)

    def tokens(self, text):
        for match in re.finditer(self.rx, text):
            if match.lastgroup:
                yield (match.lastgroup, match[0])


def token(rx, kind):
    return f"(?P<{kind}>{rx})"


def skip(rx):
    return f"({rx})"


lexer = Lexer(
    token(r"\(.*?\)", "string"),
    token(r"\d*(\d\.|\.\d)\d*", "float"),
    token(r"\d+", "int"),
    skip(r"%.*$"),
    skip(r"\s+"),
)
