"""Tests of array operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from dtypes import Name
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # [
        ("[ type", [Name(False, "marktype")]),
        # ]
        ("[ ] length", [0]),
        ("[ 1 2 3 ] length", [3]),
        # array
        ("0 array dup type exch length", [Name(False, "arraytype"), 0]),
        ("10 array dup type exch length", [Name(False, "arraytype"), 10]),
        ("10 array 0 get type", [Name(False, "nulltype")]),
        # forall
        ("[ 1 2 (a) (b) 3] {} forall", [1, 2, "a", "b", 3]),
        ("[ 1 2 (a) (b) 3 ] { dup type /integertype ne { exit } if } forall", [1, 2, "a"]),
        ("[] {} forall", []),
        # get
        ("[ 1 2 3 ] 1 get", [2]),
        # length
        ("10 array length", [10]),
        # put
        ("10 array dup 3 (a) put 3 get", ["a"]),
        ("10 array dup dup 3 (a) put 3 (b) put 3 get", ["b"]),
        ("10 array dup dup 3 (a) put save exch 3 (b) put restore 3 get", ["a"]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # ]
        ("]", "unmatchedmark"),
        ("1 2 3 (a) ]", "unmatchedmark"),
        # array
        ("array", "stackunderflow"),
        ("(a) array", "typecheck"),
        # forall
        ("[1 2 3] (a) forall", "typecheck"),
        # get
        ("[ 1 2 3 ] (a) get", "typecheck"),
        ("[ 1 2 3 ] -1 get", "rangecheck"),
        ("[ 1 2 3 ] 3 get", "rangecheck"),
        ("[] 0 get", "rangecheck"),
        # put
        ("[1 2 3] (a) 1 put", "typecheck"),
        ("[1 2 3] -1 1 put", "rangecheck"),
        ("[1 2 3] 3 1 put", "rangecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
