"""Test stilted evaluation."""

import pytest

from error import Tilted
from evaluate import evaluate
from dtypes import Name
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        ("123 (hello) 1.25", [123, "hello", 1.25]),
        ("123 /Hello 1.25", [123, Name(True, "Hello"), 1.25]),
        ("/average {add 2 div} def 40 60 average", [50.0]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        ("1 2 3 xyzzy", "undefined"),
        ("(", "syntaxerror"),
        (")", "syntaxerror"),
        ("}", "syntaxerror"),
        ("{{}", "syntaxerror"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
