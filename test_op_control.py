"""Tests of control operators for stilted."""

import pytest

from dtypes import Name
from error import StiltedError
from evaluate import evaluate
from test_helpers import compare_stacks

@pytest.mark.parametrize(
    "text, stack",
    [
        # exec
        ("12 exec", [12]),
        ("12 cvx exec cvlit", [12]),
        ("(abc) exec", ["abc"]),
        ("/xyzzy exec", [Name(True, "xyzzy")]),
        ("/xyzzy {1 2 add} def /xyzzy cvx exec", [3]),
        ("{1 2 add} exec", [3]),
        ("(1 2 add) cvx exec", [3]),
        ("/add load cvlit exec cvx", "/add load"),
        ("97 null cvx exec /null load cvlit pop", [97]),
        ("{ 97 null 98 null } exec", [97, None, 98, None]),
        # exit
        ("1 1 10 { dup 3 gt {exit} if } for", [1, 2, 3, 4]),
        ("1 10 { dup 1 add dup 3 gt {exit} if } repeat", [1, 2, 3, 4]),
        # for
        ("0 1 1 4 {add} for", [10]),
        ("0 1 1 4 [/add load] cvx for", [10]),
        ("1 2 6 {} for", [1, 3, 5]),
        ("3 -.5 1 {} for", [3.0, 2.5, 2.0, 1.5, 1.0]),
        ("10 1 5 {(a)} for", []),
        ("1 1 5 { dup 3 gt { dup } if } for", [1, 2, 3, 4, 4, 5, 5]),
        # if
        ("(a) 3 4 lt {(3 < 4)} if", ["a", "3 < 4"]),
        ("(a) 3 4 gt {(3 > 4)} if", ["a"]),
        # ifelse
        ("(a) 3 4 lt {(3 < 4)} {(3 not < 4)} ifelse", ["a", "3 < 4"]),
        ("(a) 3 4 gt {(3 > 4)} {(3 not > 4)} ifelse", ["a", "3 not > 4"]),
        # loop
        ("1 2 3 4 5 { 3 eq { exit } if } loop 99", [1, 2, 99]),
        # repeat
        ("4 {(a)} repeat", ["a", "a", "a", "a"]),
        ("1 2 3 4 3 {pop} repeat", [1]),
        ("4 {} repeat", []),
        ("99 0 {(a)} repeat", [99]),
        # stop
        ("{ 1 2 add stop } stopped 99", [3, True, 99]),
        ("{ 1 1 10 { dup 2 gt { stop } if } for } stopped 99", [1, 2, 3, True, 99]),
        # stopped
        ("12 stopped 99", [12, False, 99]),
        ("{1 2 add} stopped 99", [3, False, 99]),
        ("(1 2 add) cvx stopped 99", [3, False, 99]),
        ("/xyzzy {1 2 add} def /xyzzy cvx stopped 99", [3, False, 99]),
        ("/H{{loop}stopped Y}def/Y/pop/m/mul/a/add{load def}H 3 4 a 5 m", [35]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # exec
        ("exec", "stackunderflow"),
        # for
        ("for", "stackunderflow"),
        ("{} for", "stackunderflow"),
        ("1 {} for", "stackunderflow"),
        ("1 1 {} for", "stackunderflow"),
        ("1 1 1 [] for", "typecheck"),
        ("1 1 1 (a) for", "typecheck"),
        ("1 1 (a) {} for", "typecheck"),
        ("1 (a) 1 {} for", "typecheck"),
        ("(a) 1 1 {} for", "typecheck"),
        # forall
        ("forall", "stackunderflow"),
        ("{} forall", "stackunderflow"),
        ("123 {} forall", "typecheck"),
        ("10 dict 123 forall", "typecheck"),
        ("10 dict [] forall", "typecheck"),
        # if
        ("if", "stackunderflow"),
        ("{1} if", "stackunderflow"),
        ("1 {1} if", "typecheck"),
        ("true 1 if", "typecheck"),
        ("true [] if", "typecheck"),
        # ifelse
        ("ifelse", "stackunderflow"),
        ("{1} {2} ifelse", "stackunderflow"),
        ("1 {1} {2} ifelse", "typecheck"),
        ("true {1} 2 ifelse", "typecheck"),
        ("true 1 {2} ifelse", "typecheck"),
        ("true [1] 2 ifelse", "typecheck"),
        ("true 1 [2] ifelse", "typecheck"),
        # loop
        ("loop", "stackunderflow"),
        ("1 loop", "typecheck"),
        # repeat
        ("repeat", "stackunderflow"),
        ("{} repeat", "stackunderflow"),
        ("(a) {} repeat", "typecheck"),
        ("1 [] repeat", "typecheck"),
        ("1.5 {} repeat", "typecheck"),
        ("-2 {} repeat", "rangecheck"),
        # stop
        ("stopped", "stackunderflow")
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)

@pytest.mark.parametrize(
    "code",
    [
        "quit",
        "1 3 lt {exit} if",
        "1 3 lt {stop} if",
    ],
)
def test_system_exit(code):
    with pytest.raises(SystemExit):
        evaluate(code)
