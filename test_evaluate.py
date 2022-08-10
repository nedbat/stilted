"""Test stilted evaluation."""

import pytest

from error import StiltedError
from evaluate import evaluate
from dtypes import Name
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        ("123 (hello) 1.25", [123, "hello", 1.25]),
        ("123 /Hello 1.25", [123, Name(True, "Hello"), 1.25]),
        ("/average {add 2 div} def 40 60 average", [50.0]),
        ("""
            /xform { transform 2 { round .6 add exch } repeat } def
            matrix identmatrix setmatrix 10 20 translate
            1 2 xform
        """, [11.6, 22.6]),
        # Error handlers will be executed from errordict.
        (
            "errordict /undefined { (HELLO) } put xyzzy",
            "/xyzzy cvx (HELLO)",
        ),
        # Errors will restore the stack and push the object.
        (
            "errordict /typecheck { (!!!) } put 1 (a) add",
            "1 (a) /add load (!!!)",
        ),
        (
            "errordict /typecheck { (!!!) } put (a) 1 10 { hello } for",
            "(a) 1 10 { hello } /for load (!!!)",
        ),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        ("1 2 3 xyzzy", "undefined"),
        ("(", "syntaxerror"),
        (")", "syntaxerror"),
        ("}", "syntaxerror"),
        ("{{}", "syntaxerror"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
