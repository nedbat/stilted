"""Tests of control operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate


@pytest.mark.parametrize(
    "text, stack",
    [
        # if
        ("(a) 3 4 lt {(3 < 4)} if", ["a", "3 < 4"]),
        ("(a) 3 4 gt {(3 > 4)} if", ["a"]),
        # ifelse
        ("(a) 3 4 lt {(3 < 4)} {(3 not < 4)} ifelse", ["a", "3 < 4"]),
        ("(a) 3 4 gt {(3 > 4)} {(3 not > 4)} ifelse", ["a", "3 not > 4"]),
    ],
)
def test_evaluate(text, stack):
    assert evaluate(text).ostack == stack


@pytest.mark.parametrize(
    "text, error",
    [
        # if
        ("if", "stackunderflow"),
        ("{1} if", "stackunderflow"),
        ("1 {1} if", "typecheck"),
        ("true 1 if", "typecheck"),
        # ifelse
        ("ifelse", "stackunderflow"),
        ("{1} {2} ifelse", "stackunderflow"),
        ("1 {1} {2} ifelse", "typecheck"),
        ("true {1} 2 ifelse", "typecheck"),
        ("true 1 {2} ifelse", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
