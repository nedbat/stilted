"""Tests of relational operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate

from test_helpers import compare_stacks

@pytest.mark.parametrize(
    "text, stack",
    [
        # and
        ("true true and", [True]),
        ("true false and", [False]),
        ("false false and", [False]),
        ("99 1 and", [1]),
        ("52 7 and", [4]),
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
        # not
        ("true not", [False]),
        ("false not", [True]),
        ("52 not", [-53]),
        ("-53 not", [52]),
        # or
        ("true true or", [True]),
        ("true false or", [True]),
        ("false false or", [False]),
        ("17 5 or", [21]),
        # xor
        ("true true xor", [False]),
        ("true false xor", [True]),
        ("false false xor", [False]),
        ("7 3 xor", [4]),
        ("12 3 xor", [15]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


OP1 = ["not"]

@pytest.mark.parametrize("opname", OP1)
def test_one_arg_stackunderflow(opname):
    with pytest.raises(Tilted, match="stackunderflow"):
        evaluate(opname)

@pytest.mark.parametrize("opname", OP1)
def test_one_arg_errors(opname):
    with pytest.raises(Tilted, match="typecheck"):
        evaluate(f"(a) {opname}")


OP2 = ["and", "eq", "ge", "gt", "le", "lt", "ne", "or", "xor"]

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
