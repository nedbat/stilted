"""Tests of matrix and coordinate operators for stilted."""

from math import sqrt

import pytest

from error import Tilted
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # concat
        (
            "20 30 matrix identmatrix scale concat matrix currentmatrix",
            "20 30 scale matrix currentmatrix",
        ),
        # concatmatrix
        (
            "10 20 matrix translate 3 4 matrix scale matrix concatmatrix",
            "matrix identmatrix setmatrix 3 4 scale 10 20 translate matrix currentmatrix",
        ),
        # currentmatrix
        ("matrix currentmatrix length", [6]),
        ("matrix currentmatrix 1 get", [0.0]),
        ("matrix currentmatrix dup 4 get exch 5 get", [0.0, 0.0]),
        # defaultmatrix
        ("10 10 scale matrix defaultmatrix", "matrix currentmatrix"),
        # dtransform
        ("matrix identmatrix setmatrix 0 0 dtransform", [0.0, 0.0]),
        ("matrix identmatrix setmatrix 100 200 dtransform", [100.0, 200.0]),
        ("matrix identmatrix setmatrix 17 42 translate 0 0 dtransform", [0.0, 0.0]),
        ("matrix identmatrix setmatrix 90 rotate 10 10 translate 100 200 dtransform", [-200.0, 100.0]),
        ("matrix identmatrix setmatrix 2 3 scale 10 10 translate 100 200 dtransform", [200.0, 600.0]),
        ("100 200 2 3 10 10 matrix translate scale dtransform", [200.0, 600.0]),
        # identmatrix
        ("6 array identmatrix aload pop", [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]),
        # idtransform
        ("matrix identmatrix setmatrix 0 0 idtransform", [0.0, 0.0]),
        ("matrix identmatrix setmatrix 100 200 idtransform", [100.0, 200.0]),
        ("matrix identmatrix setmatrix 17 42 translate 17 42 idtransform", [17.0, 42.0]),
        ("matrix identmatrix setmatrix 90 rotate 10 10 translate -200 100 idtransform", [100.0, 200.0]),
        ("matrix identmatrix setmatrix 2 3 scale 10 10 translate 200 600 idtransform", [100.0, 200.0]),
        ("200 600 2 3 10 10 matrix translate scale idtransform", [100.0, 200.0]),
        # initmatrix
        ("10 10 scale initmatrix matrix currentmatrix", "matrix currentmatrix"),
        # invertmatrix
        ("200 600 2 3 matrix scale matrix invertmatrix transform", [100.0, 200.0]),
        # itransform
        ("matrix identmatrix setmatrix 0 0 itransform", [0.0, 0.0]),
        ("matrix identmatrix setmatrix 100 200 itransform", [100.0, 200.0]),
        ("matrix identmatrix setmatrix 17 42 translate 17 42 itransform", [0.0, 0.0]),
        ("matrix identmatrix setmatrix 90 rotate -200 100 itransform", [100.0, 200.0]),
        ("matrix identmatrix setmatrix 2 3 scale 200 600 itransform", [100.0, 200.0]),
        ("200 600 2 3 matrix scale itransform", [100.0, 200.0]),
        # matrix
        ("matrix aload pop", [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]),
        # rotate
        ("30 matrix rotate aload pop", [sqrt(3)/2, 0.5, -0.5, sqrt(3)/2, 0.0, 0.0]),
        # scale
        ("17 42 matrix scale aload pop", [17.0, 0.0, 0.0, 42.0, 0.0, 0.0]),
        # setmatrix
        ("[1 2 3 4 5 6] setmatrix matrix currentmatrix aload pop", [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]),
        # transform
        ("matrix identmatrix setmatrix 0 0 transform", [0.0, 0.0]),
        ("matrix identmatrix setmatrix 100 200 transform", [100.0, 200.0]),
        ("matrix identmatrix setmatrix 17 42 translate 0 0 transform", [17.0, 42.0]),
        ("matrix identmatrix setmatrix 90 rotate 100 200 transform", [-200.0, 100.0]),
        ("matrix identmatrix setmatrix 2 3 scale 100 200 transform", [200.0, 600.0]),
        ("100 200 2 3 matrix scale transform", [200.0, 600.0]),
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
        # concat
        ("concat", "stackunderflow"),
        ("1 concat", "typecheck"),
        ("[1] concat", "rangecheck"),
        # concatmatrix
        ("concatmatrix", "stackunderflow"),
        ("matrix concatmatrix", "stackunderflow"),
        ("matrix matrix concatmatrix", "stackunderflow"),
        ("1 matrix matrix concatmatrix", "typecheck"),
        ("matrix 1 matrix concatmatrix", "typecheck"),
        ("matrix matrix 1 concatmatrix", "typecheck"),
        ("[1] matrix matrix concatmatrix", "rangecheck"),
        ("matrix [1] matrix concatmatrix", "rangecheck"),
        ("matrix matrix [1] concatmatrix", "rangecheck"),
        # currentmatrix
        ("currentmatrix", "stackunderflow"),
        ("123 currentmatrix", "typecheck"),
        ("5 array currentmatrix", "rangecheck"),
        ("7 array currentmatrix", "rangecheck"),
        # defaultmatrix
        ("defaultmatrix", "stackunderflow"),
        ("1 defaultmatrix", "typecheck"),
        ("[1] defaultmatrix", "rangecheck"),
        # dtransform
        ("dtransform", "stackunderflow"),
        ("1 dtransform", "stackunderflow"),
        ("(a) 1 dtransform", "typecheck"),
        ("1 (a) dtransform", "typecheck"),
        ("(a) 1 matrix dtransform", "typecheck"),
        ("1 (a) matrix dtransform", "typecheck"),
        ("1 1 [1] dtransform", "rangecheck"),
        # identmatrix
        ("identmatrix", "stackunderflow"),
        ("123 identmatrix", "typecheck"),
        ("5 array identmatrix", "rangecheck"),
        # idtransform
        ("idtransform", "stackunderflow"),
        ("1 idtransform", "stackunderflow"),
        ("(a) 1 idtransform", "typecheck"),
        ("1 (a) idtransform", "typecheck"),
        ("(a) 1 matrix idtransform", "typecheck"),
        ("1 (a) matrix idtransform", "typecheck"),
        ("1 1 [1] idtransform", "rangecheck"),
        ("0 0 [0 0 0 0 0 0] idtransform", "undefinedresult"),
        # invertmatrix
        ("invertmatrix", "stackunderflow"),
        ("matrix invertmatrix", "stackunderflow"),
        ("1 matrix invertmatrix", "typecheck"),
        ("matrix 1 invertmatrix", "typecheck"),
        ("[1] matrix invertmatrix", "rangecheck"),
        ("matrix [1] invertmatrix", "rangecheck"),
        ("[0 0 0 0 0 0] matrix invertmatrix", "undefinedresult"),
        # itransform
        ("itransform", "stackunderflow"),
        ("1 itransform", "stackunderflow"),
        ("(a) 1 itransform", "typecheck"),
        ("1 (a) itransform", "typecheck"),
        ("(a) 1 matrix itransform", "typecheck"),
        ("1 (a) matrix itransform", "typecheck"),
        ("1 1 [1] itransform", "rangecheck"),
        ("0 0 [0 0 0 0 0 0] itransform", "undefinedresult"),
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
        # setmatrix
        ("setmatrix", "stackunderflow"),
        ("123 setmatrix", "typecheck"),
        ("[1] setmatrix", "rangecheck"),
        # transform
        ("transform", "stackunderflow"),
        ("1 transform", "stackunderflow"),
        ("(a) 1 transform", "typecheck"),
        ("1 (a) transform", "typecheck"),
        ("(a) 1 matrix transform", "typecheck"),
        ("1 (a) matrix transform", "typecheck"),
        ("1 1 [1] transform", "rangecheck"),
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
