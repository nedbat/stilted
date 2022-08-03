"""Tests of stilted's lexical analyzer."""

import pytest

from error import Tilted
from lex import lexer, Name
from test_helpers import compare_stacks

@pytest.mark.parametrize(
    "text, toks",
    [
        ("123", [123]),
        ("-123 +456", [-123, 456]),
        ("(hello)", ["hello"]),
        ("(hello 5%)  % five", ["hello 5%"]),
        (".125 -3.125 +314.", [0.125, -3.125, 314.0]),
        ("% A comment\n123", [123]),
        ("()", [""]),
        (r"(\)) 123", [")", 123]),
        (r"(\nHi\101\t\)) 123", ["\nHiA\t)", 123]),
        ("(one\ntwo)", ["one\ntwo"]),
        ("(one\\\nstill one)", ["onestill one"]),
        (r"(\1\2\34\034\0053)", ["\x01\x02\x1c\x1c\x053"]),
        ("/Hello there", [Name(True, "Hello"), Name(False, "there")]),
        ("/Hello/there", [Name(True, "Hello"), Name(True, "there")]),
        ("[123]", [Name(False, "["), 123, Name(False, "]")]),
        ("{abc {foo} if}", list(map(Name.from_string, "{ abc { foo } if }".split()))),
        (
            "abc Offset $$ 23A 13-456 a.b $MyDict @pattern",
            list(map(Name.from_string, "abc Offset $$ 23A 13-456 a.b $MyDict @pattern".split())),
        ),
        ("<901fa3>", ["\x90\x1f\xa3"]),
        ("<9 01fa>123", ["\x90\x1f\xa0", 123]),
    ],
)
def test_lexer(text, toks):
    compare_stacks(list(lexer.tokens(text)), toks)


@pytest.mark.parametrize(
    "text",
    [
        ")",
        "123)",
        "<hello there>",
        "<",
        ">",
    ],
)
def test_lexer_syntaxerror(text):
    with pytest.raises(Tilted, match="syntaxerror"):
        list(lexer.tokens(text))
