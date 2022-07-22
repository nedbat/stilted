"""Tests of object model operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from dtypes import Name
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # cvlit
        ("{hello} cvlit xcheck", [False]),
        # cvx
        ("/Hello cvx xcheck", [True]),
        # type
        ("true type", [Name(False, "boolean")]),
        ("123 type", [Name(False, "integer")]),
        ("mark type", [Name(False, "mark")]),
        ("/Name type", [Name(False, "name")]),
        ("12.3 type", [Name(False, "real")]),
        ("(hello) type", [Name(False, "string")]),
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
        # type
        ("type", "stackunderflow"),
        # xcheck
        ("xcheck", "stackunderflow"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
