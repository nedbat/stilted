"""Tests of object model operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from dtypes import MARK
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # cvlit
        ("{hello} cvlit xcheck", [False]),
        # cvx
        ("/Hello cvx xcheck", [True]),
        # xcheck
        ("/Hello xcheck", [False]),
        ("{hello} xcheck", [True]),
        ("123 xcheck", [False]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # cvlit
        ("cvlit", "stackunderflow"),
        # cvx
        ("cvx", "stackunderflow"),
        # xcheck
        ("xcheck", "stackunderflow"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
