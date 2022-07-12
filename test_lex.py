import pytest

from lex import lexer


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
    ],
)
def test_lexer(text, toks):
    assert list(lexer.tokens(text)) == toks
