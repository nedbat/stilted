"""Tests of matrix and coordinate operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # currentmatrix
        ("matrix currentmatrix length", [6]),
        ("matrix currentmatrix 1 get", [0.0]),
        ("matrix currentmatrix dup 4 get exch 5 get", [0.0, 0.0]),
        # identmatrix
        ("6 array identmatrix aload pop", [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]),
        # matrix
        ("matrix aload pop", [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]),
        # rotate
        ("30 matrix rotate 1 get 0.5 sub abs 0.000001 lt", [True]),
        ("30 matrix rotate 2 get -0.5 sub abs 0.000001 lt", [True]),
        # scale
        ("17 42 matrix scale aload pop", [17.0, 0.0, 0.0, 42.0, 0.0, 0.0]),
        # translate
        ("17 42 translate matrix currentmatrix dup 4 get exch 5 get", [17.0, 42.0]),
        ("17 42 matrix translate aload pop", [1.0, 0.0, 0.0, 1.0, 17.0, 42.0]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # currentmatrix
        ("currentmatrix", "stackunderflow"),
        ("123 currentmatrix", "typecheck"),
        ("5 array currentmatrix", "rangecheck"),
        ("7 array currentmatrix", "rangecheck"),
        # identmatrix
        ("identmatrix", "stackunderflow"),
        ("123 identmatrix", "typecheck"),
        ("5 array identmatrix", "rangecheck"),
        # rotate
        ("rotate", "stackunderflow"),
        ("(a) rotate", "typecheck"),
        ("(a) matrix rotate", "typecheck"),
        ("1 [1] rotate", "rangecheck"),
        # scale
        ("scale", "stackunderflow"),
        ("1 scale", "stackunderflow"),
        ("(a) 1 scale", "typecheck"),
        ("1 (a) scale", "typecheck"),
        ("1 (a) matrix scale", "typecheck"),
        ("(a) 1 matrix scale", "typecheck"),
        ("1 1 [1] scale", "rangecheck"),
        # translate
        ("translate", "stackunderflow"),
        ("1 translate", "stackunderflow"),
        ("(a) 1 translate", "typecheck"),
        ("1 (a) translate", "typecheck"),
        ("1 (a) matrix translate", "typecheck"),
        ("(a) 1 matrix translate", "typecheck"),
        ("1 1 [1] translate", "rangecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
