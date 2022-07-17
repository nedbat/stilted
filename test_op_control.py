"""Tests of control operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate


@pytest.mark.parametrize(
    "text, stack",
    [
        # for
        ("0 1 1 4 {add} for", [10]),
        ("1 2 6 {} for", [1, 3, 5]),
        ("3 -.5 1 {} for", [3.0, 2.5, 2.0, 1.5, 1.0]),
        ("10 1 5 {(a)} for", []),
        # if
        ("(a) 3 4 lt {(3 < 4)} if", ["a", "3 < 4"]),
        ("(a) 3 4 gt {(3 > 4)} if", ["a"]),
        # ifelse
        ("(a) 3 4 lt {(3 < 4)} {(3 not < 4)} ifelse", ["a", "3 < 4"]),
        ("(a) 3 4 gt {(3 > 4)} {(3 not > 4)} ifelse", ["a", "3 not > 4"]),
        # repeat
        ("4 {(a)} repeat", ["a", "a", "a", "a"]),
        ("1 2 3 4 3 {pop} repeat", [1]),
        ("4 {} repeat", []),
        ("99 0 {(a)} repeat", [99]),
    ],
)
def test_evaluate(text, stack):
    assert evaluate(text).ostack == stack


@pytest.mark.parametrize(
    "text, error",
    [
        # for
        ("for", "stackunderflow"),
        ("{} for", "stackunderflow"),
        ("1 {} for", "stackunderflow"),
        ("1 1 {} for", "stackunderflow"),
        ("1 1 1 (a) for", "typecheck"),
        ("1 1 (a) {} for", "typecheck"),
        ("1 (a) 1 {} for", "typecheck"),
        ("(a) 1 1 {} for", "typecheck"),
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
        # repeat
        ("repeat", "stackunderflow"),
        ("{} repeat", "stackunderflow"),
        ("(a) {} repeat", "typecheck"),
        ("1.5 {} repeat", "typecheck"),
        ("-2 {} repeat", "rangecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)