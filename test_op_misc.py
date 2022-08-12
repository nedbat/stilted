"""Tests of miscellaneous operators for Stilted."""

import pytest

from dtypes import Name
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # usertime
        ("usertime type", [Name(False, "integertype")]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)
