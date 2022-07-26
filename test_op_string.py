"""Tests of string operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from dtypes import Name
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # forall
        ("(hello) {} forall", [104, 101, 108, 108, 111]),
        ("0 (hello) { add } forall", [532]),
        ("(ABCdef) { dup (a) 0 get ge {exit} if } forall", [65, 66, 67, 100]),
        # get
        ("(hello) 2 get", [108]),
        # length
        ("(hello) length", [5]),
        ("() length", [0]),
        ("/hello length", [5]),
        # put
        ("(hello) dup 2 88 put", ["heXlo"]),
        ("(hello) dup save exch 2 88 put restore", ["heXlo"]),  # strings don't restore
        # string
        ("5 string", ["\0\0\0\0\0"]),
        ("0 string", [""]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # forall
        ("(hello) 123 forall", "typecheck"),
        # get
        ("(hello) (a) get", "typecheck"),
        ("(hello) 10 get", "rangecheck"),
        ("(hello) -10 get", "rangecheck"),
        # put
        ("(hello) (a) 123 put", "typecheck"),
        ("(hello) 2 (a) put", "typecheck"),
        ("(hello) 10 123 put", "rangecheck"),
        ("(hello) -10 123 put", "rangecheck"),
        # string
        ("string", "stackunderflow"),
        ("-1 string", "rangecheck"),
        ("3.4 string", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
