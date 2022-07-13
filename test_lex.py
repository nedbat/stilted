"""Tests of stilted's lexical analyzer."""

import re

import pytest

from lex import lexer, Name


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
        (r"(\nHi\101\)) 123", ["\nHiA)", 123]),
        ("(one\ntwo)", ["one\ntwo"]),
        ("(one\\\nstill one)", ["onestill one"]),
        (r"(\1\2\34\034\0053)", ["\x01\x02\x1c\x1c\x053"]),
        ("/Hello there", [Name("Hello", True), Name("there")]),
        ("/Hello/there", [Name("Hello", True), Name("there", True)]),
        ("[123]", [Name("["), 123, Name("]")]),
        ("{abc {foo} if}", list(map(Name, "{ abc { foo } if }".split()))),
        (
            "abc Offset $$ 23A 13-456 a.b $MyDict @pattern",
            list(map(Name, "abc Offset $$ 23A 13-456 a.b $MyDict @pattern".split())),
        ),
    ],
)
def test_lexer(text, toks):
    assert list(lexer.tokens(text)) == toks


@pytest.mark.parametrize(
    "text, error",
    [
        (")", ")"),
        ("123)", ")"),
    ],
)
def test_lexer_error(text, error):
    with pytest.raises(Exception, match=re.escape(f"Lexical error: {error!r}")):
        list(lexer.tokens(text))
