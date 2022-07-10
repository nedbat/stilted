import pytest

from lex import lexer


@pytest.mark.parametrize(
    "text, toks",
    [
        ("123", [("int", 123)]),
        ("-123 +456", [("int", -123), ("int", 456)]),
        ("(hello)", [("string", "(hello)")]),
        ("(hello 5%)  % five", [("string", "(hello 5%)")]),
        (".125 -3.125 +314.", [("float", 0.125), ("float", -3.125), ("float", 314.0)]),
        ("% A comment\n123", [("int", 123)]),
    ],
)
def test_lexer(text, toks):
    assert list(lexer.tokens(text)) == toks
