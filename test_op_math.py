"""Tests of math operators for stilted."""

import pytest

from error import StiltedError
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
        # atan
        ("0 1 atan", [0.0]),
        ("1 0 atan", [90.0]),
        ("-100 0 atan", [270.0]),
        ("4 4 atan", [45.0]),
        ("-4 4 atan", [315.0]),
        ("-4 -4 atan", [225.0]),
        ("4 -4 atan", [135.0]),
        # ceiling
        ("3.2 ceiling", [4.0]),
        ("-4.8 ceiling", [-4.0]),
        ("99 ceiling", [99]),
        # cos
        ("0 cos", [1.0]),
        ("90 cos 0.0 _isclose", [True]),
        ("135 cos -1 2 sqrt div _isclose", [True]),
        # div
        ("3 2 div", [1.5]),
        ("4 2 div", [2.0]),
        # exp
        ("9 0.5 exp", [3.0]),
        ("-9 -1 exp", [-0.1111111111111]),
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
        # rand, rrand, srand
        ("17 srand rand rand rand rand", [1778837931, 1303193990, 1570340887, 1243931546]),
        ("17 srand rand rand 17 srand rand rand", [1778837931, 1303193990, 1778837931, 1303193990]),
        ("""
            17 srand rand pop rand pop
            /r rrand def
            r srand rand rand
            r srand rand rand
            """,
            [2102238088, 3827999, 2102238088, 3827999],
        ),
        # round
        ("3.2 round", [3.0]),
        ("6.5 round", [7.0]),
        ("-4.8 round", [-5.0]),
        ("-6.5 round", [-6.0]),
        ("99 round", [99]),
        # sin
        ("0 sin", [0.0]),
        ("90 sin 1.0 _isclose", [True]),
        ("-45 sin -1 2 sqrt div _isclose", [True]),
        # sqrt
        ("150.0625 sqrt", [12.25]),
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


OP1 = ["abs", "ceiling", "cos", "floor", "neg", "round", "sin", "srand", "sqrt", "truncate"]

@pytest.mark.parametrize("opname", OP1)
def test_one_arg_stackunderflow(opname):
    with pytest.raises(StiltedError, match="stackunderflow"):
        evaluate(opname)

@pytest.mark.parametrize("opname", OP1)
def test_one_arg_errors(opname):
    with pytest.raises(StiltedError, match="typecheck"):
        evaluate(f"(a) {opname}")

OP2 = ["add", "atan", "div", "exp", "idiv", "mod", "mul", "sub"]

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_stackunderflow1(opname):
    with pytest.raises(StiltedError, match="stackunderflow"):
        evaluate(opname)

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_stackunderflow2(opname):
    with pytest.raises(StiltedError, match="stackunderflow"):
        evaluate(f"1 {opname}")

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_typecheck1(opname):
    with pytest.raises(StiltedError, match="typecheck"):
        evaluate(f"1 (a) {opname}")

@pytest.mark.parametrize("opname", OP2)
def test_two_arg_typecheck2(opname):
    with pytest.raises(StiltedError, match="typecheck"):
        evaluate(f"(a) 1 {opname}")


@pytest.mark.parametrize(
    "text, error",
    [
        # # atan, meh let it be zero.
        # ("0 0 atan", "undefinedresult"),
        # exp
        ("-1 1.5 exp", "undefinedresult"),
        # sqrt
        ("-1 sqrt", "rangecheck"),
        # srand
        ("1.1 srand", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
