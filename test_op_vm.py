"""Tests of VM operators for stilted."""

import pytest

from error import StiltedError
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        ("/foo 17 def save /foo 23 def foo exch restore foo", [23, 17]),
        ("/d 10 dict def d /foo 17 put save d /foo 23 put d begin foo exch restore foo", [23, 17]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        ("restore", "stackunderflow"),
        ("123 restore", "typecheck"),
        ("save dup restore restore", "invalidrestore"),
        ("save save exch restore restore", "invalidrestore"),
        ("save 10 dict exch restore", "invalidrestore"),
        ("save 10 dict begin restore", "invalidrestore"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
