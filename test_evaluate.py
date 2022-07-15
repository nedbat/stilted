"""Tests of stack evaluation for stilted."""

import pytest

from evaluate import evaluate
from lex import Name


@pytest.mark.parametrize(
    "text, stack",
    [
        ("123 (hello) 1.25", [123, "hello", 1.25]),
        ("123 /Hello 1.25", [123, Name("Hello", True), 1.25]),
        # copy
        ("(a) (b) (c) 2 copy", ["a", "b", "c", "b", "c"]),
        ("(a) (b) (c) 0 copy", ["a", "b", "c"]),
        # dup
        ("1 123 dup", [1, 123, 123]),
        # exch
        ("1 123 456 exch", [1, 456, 123]),
        # index
        ("(a) (b) (c) (d) 0 index", ["a", "b", "c", "d", "d"]),
        ("(a) (b) (c) (d) 3 index", ["a", "b", "c", "d", "a"]),
        # pop
        ("1 123 pop", [1]),
        # roll
        ("(a) (b) (c) 3 -1 roll", ["b", "c", "a"]),
        ("(a) (b) (c) 3 1 roll", ["c", "a", "b"]),
        ("(a) (b) (c) 3 0 roll", ["a", "b", "c"]),
        # def
        ("1 /hello (there) def 2 hello", [1, 2, "there"]),
    ],
)
def test_evaluate(text, stack):
    assert evaluate(text).ostack == stack
