"""Tests of relational operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate


@pytest.mark.parametrize(
    "text, stack",
    [
        # eq
        ("4.0 4 eq", [True]),
        ("4.0 5 eq", [False]),
        ("(abc) (abc) eq", [True]),
        ("(abc) (abz) eq", [False]),
        ("(abc) /abc eq", [True]),
        ("(abc) /abz eq", [False]),
        #("[1 2 3] dup eq", [True]),
        #("[1 2 3] [1 2 3] eq", [False]),
        # ge
        ("4.0 4 ge", [True]),
        ("4.2 4 ge", [True]),
        ("4.2 5 ge", [False]),
        ("(abc) (d) ge", [False]),
        ("(aba) (ab) ge", [True]),
        ("(aba) (aba) ge", [True]),
        # gt
        ("4.0 4 gt", [False]),
        ("4.2 4 gt", [True]),
        ("4.2 5 gt", [False]),
        ("(abc) (d) gt", [False]),
        ("(aba) (ab) gt", [True]),
        ("(aba) (aba) gt", [False]),
        # le
        ("4.0 4 le", [True]),
        ("4.2 4 le", [False]),
        ("4.2 5 le", [True]),
        ("(abc) (d) le", [True]),
        ("(aba) (ab) le", [False]),
        ("(aba) (aba) le", [True]),
        # lt
        ("4.0 4 lt", [False]),
        ("4.2 4 lt", [False]),
        ("4.2 5 lt", [True]),
        ("(abc) (d) lt", [True]),
        ("(aba) (ab) lt", [False]),
        ("(aba) (aba) lt", [False]),
        # ne
        ("4.0 4 ne", [False]),
        ("4.0 5 ne", [True]),
        ("(abc) (abc) ne", [False]),
        ("(abc) (abz) ne", [True]),
        ("(abc) /abc ne", [False]),
        ("(abc) /abz ne", [True]),
    ],
)
def test_evaluate(text, stack):
    results = evaluate(text).ostack
    assert results == stack


OP2 = ["eq", "ge", "gt", "le", "lt", "ne"]

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_stackunderflow1(opname):
    with pytest.raises(Tilted, match="stackunderflow"):
        evaluate(opname)

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_stackunderflow2(opname):
    with pytest.raises(Tilted, match="stackunderflow"):
        evaluate(f"1 {opname}")

@pytest.mark.parametrize("opname", OP2)
def test_mismatch(opname):
    with pytest.raises(Tilted, match="typecheck"):
        evaluate(f"1 (abc) {opname}")
    with pytest.raises(Tilted, match="typecheck"):
        evaluate(f"(abc) 1 {opname}")
