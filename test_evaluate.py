"""Tests of stack evaluation for stilted."""

import pytest

from evaluate import evaluate
from lex import Name


@pytest.mark.parametrize(
    "text, stack",
    [
        ("123 (hello) 1.25", [123, "hello", 1.25]),
        ("123 /Hello 1.25", [123, Name("Hello", True), 1.25]),
    ],
)
def test_evaluate(text, stack):
    assert evaluate(text) == stack
