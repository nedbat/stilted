"""Tests of miscellaneous operators for Stilted."""

import pytest

from dtypes import Name
from error import StiltedError
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # bind
        ("[] bind", "[]"),
        ("{1 2 add {mul} 3} bind", "[ 1 2 /add load [ /mul load ] cvx 3] cvx"),
        ("{1 2 /add {/mul} 3} bind", "[ 1 2 /add [ /mul ] cvx 3] cvx"),
        ("[1 2 /add cvx [/mul cvx] 3] bind", "[ 1 2 /add load [ /mul load ] 3]"),
        ("{ xyzzy product } bind", "{ xyzzy product }"),
        # usertime
        ("usertime type", [Name(False, "integertype")]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # bind
        ("bind", "stackunderflow"),
        ("1 bind", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
