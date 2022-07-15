"""Tests of stack evaluation for stilted."""

import pytest

from evaluate import evaluate
from lex import Name


@pytest.mark.parametrize(
    "text, stack",
    [
        ("123 (hello) 1.25", [123, "hello", 1.25]),
        ("123 /Hello 1.25", [123, Name("Hello", True), 1.25]),
        ("1 123 dup", [1, 123, 123]),
        ("1 123 456 exch", [1, 456, 123]),
        ("1 123 pop", [1]),
        ("1 /hello (there) def 2 hello", [1, 2, "there"]),
    ],
)
def test_evaluate(text, stack):
    assert evaluate(text).ostack == stack
