"""Helpers for tests for Stilted."""

from typing import Any

from dtypes import from_py, Object
from evaluate import evaluate

def compare_stacks(stk1: list[Object], stk2: list[Any] | str):
    """
    Compare stacks for tests.

    `stk1` is an ostack from an evaluation.
    `stk2` is either a list of Python objects, or a string to evaluate to get
    another ostack.

    The two must be equal.
    """
    if isinstance(stk2, str):
        stk2 = evaluate(stk2).ostack
    assert len(stk1) == len(stk2)
    for v1, v2 in zip(stk1, stk2):
        if not isinstance(v2, Object):
            v2 = from_py(v2)
        assert type(v1) == type(v2)
        assert v1 == v2
