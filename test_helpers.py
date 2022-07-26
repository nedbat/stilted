"""Helpers for tests for Stilted."""

from dtypes import from_py, Object

def compare_stacks(stk1, stk2):
    assert len(stk1) == len(stk2)
    for v1, v2 in zip(stk1, stk2):
        if not isinstance(v2, Object):
            v2 = from_py(v2)
        assert v1 == v2
