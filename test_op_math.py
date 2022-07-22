"""Tests of math operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # abs
        ("3 abs", [3]),
        ("-3 abs", [3]),
        ("-3.5 abs", [3.5]),
        # add
        ("3 4 add", [7]),
        ("3 4.5 add", [7.5]),
        ("3.5 4.5 add", [8.0]),
        # ceiling
        ("3.2 ceiling", [4.0]),
        ("-4.8 ceiling", [-4.0]),
        ("99 ceiling", [99]),
        # div
        ("3 2 div", [1.5]),
        ("4 2 div", [2.0]),
        # floor
        ("3.2 floor", [3.0]),
        ("-4.8 floor", [-5.0]),
        ("99 floor", [99]),
        # idiv
        ("3 2 idiv", [1]),
        ("4 2 idiv", [2]),
        ("-5 2 idiv", [-2]),
        # mod
        ("5 3 mod", [2]),
        ("5 2 mod", [1]),
        ("-5 3 mod", [-2]),
        # mul
        ("3 2 mul", [6]),
        ("1.5 3.5 mul", [5.25]),
        ("2 3.5 mul", [7.0]),
        # neg
        ("4.5 neg", [-4.5]),
        ("-3 neg", [3]),
        # round
        ("3.2 round", [3.0]),
        ("6.5 round", [7.0]),
        ("-4.8 round", [-5.0]),
        ("-6.5 round", [-6.0]),
        ("99 round", [99]),
        # sub
        ("3 4 sub", [-1]),
        ("3.5 1.5 sub", [2.0]),
        # truncate
        ("3.2 truncate", [3.0]),
        ("-4.8 truncate", [-4.0]),
        ("99 truncate", [99]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


OP1 = ["abs", "ceiling", "floor", "neg", "round", "truncate"]

@pytest.mark.parametrize("opname", OP1)
def test_one_arg_stackunderflow(opname):
    with pytest.raises(Tilted, match="stackunderflow"):
        evaluate(opname)

@pytest.mark.parametrize("opname", OP1)
def test_one_arg_errors(opname):
    with pytest.raises(Tilted, match="typecheck"):
        evaluate(f"(a) {opname}")

OP2 = ["add", "div", "idiv", "mod", "mul", "sub"]

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_stackunderflow1(opname):
    with pytest.raises(Tilted, match="stackunderflow"):
        evaluate(opname)

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_stackunderflow2(opname):
    with pytest.raises(Tilted, match="stackunderflow"):
        evaluate(f"1 {opname}")

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_typecheck1(opname):
    with pytest.raises(Tilted, match="typecheck"):
        evaluate(f"1 (a) {opname}")

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_typecheck2(opname):
    with pytest.raises(Tilted, match="typecheck"):
        evaluate(f"(a) 1 {opname}")
