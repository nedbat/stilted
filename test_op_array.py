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
        # aload
        ("[1 2 (a)] aload length", [1, 2, "a", 3]),
        # array
        ("0 array dup type exch length", [Name(False, "arraytype"), 0]),
        ("10 array dup type exch length", [Name(False, "arraytype"), 10]),
        ("10 array 0 get type", [Name(False, "nulltype")]),
        # astore
        ("1 2 3 4 3 array astore length", [1, 3]),
        ("99 1 2 3 4 3 array astore {add} forall", [99, 10]),
        # copy
        ("/a 5 array def [1 2 3] a copy {} forall", [1, 2, 3]),
        # forall
        ("[ 1 2 (a) (b) 3] {} forall", [1, 2, "a", "b", 3]),
        ("[ 1 2 (a) (b) 3 ] { dup type /integertype ne { exit } if } forall", [1, 2, "a"]),
        ("[] {} forall", []),
        # get
        ("[ 1 2 3 ] 1 get", [2]),
        # getinterval
        ("[9 8 7 6 5] 1 3 getinterval dup length exch 0 get", [3, 8]),
        ("[9 8 7 6 5] dup 1 3 getinterval 0 99 put {} forall", [9, 99, 7, 6, 5]),
        # length
        ("10 array length", [10]),
        # put
        ("10 array dup 3 (a) put 3 get", ["a"]),
        ("10 array dup dup 3 (a) put 3 (b) put 3 get", ["b"]),
        ("10 array dup dup 3 (a) put save exch 3 (b) put restore 3 get", ["a"]),
        # putinterval
        ("[9 8 7 6 5] dup 1 [1 2 3] putinterval {} forall", [9, 1, 2, 3, 5]),
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
        # aload
        ("aload", "stackunderflow"),
        ("123 aload", "typecheck"),
        # array
        ("array", "stackunderflow"),
        ("(a) array", "typecheck"),
        # astore
        ("astore", "stackunderflow"),
        ("123 astore", "typecheck"),
        ("[1] astore", "stackunderflow"),
        # copy
        ("[1 2 3] 3.5 copy", "typecheck"),
        ("[1 2 3] [1] copy", "rangecheck"),
        # forall
        ("[1 2 3] (a) forall", "typecheck"),
        # get
        ("[ 1 2 3 ] (a) get", "typecheck"),
        ("[ 1 2 3 ] -1 get", "rangecheck"),
        ("[ 1 2 3 ] 3 get", "rangecheck"),
        ("[] 0 get", "rangecheck"),
        # getinterval
        ("[1 2 3] 1 (a) getinterval", "typecheck"),
        ("[1 2 3] (a) 1 getinterval", "typecheck"),
        # put
        ("[1 2 3] (a) 1 put", "typecheck"),
        ("[1 2 3] -1 1 put", "rangecheck"),
        ("[1 2 3] 3 1 put", "rangecheck"),
        # putinterval
        ("[1 2 3] 1 (a) putinterval", "typecheck"),
        ("[1 2 3] -1 [1] putinterval", "rangecheck"),
        ("[1 2 3] 10 [1] putinterval", "rangecheck"),
        ("[1 2 3] 2 [7 8 9] putinterval", "rangecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
