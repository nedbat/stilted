"""Tests of string operators for stilted."""

import pytest

from dtypes import Name
from error import Tilted
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # cvn
        ("(xyzzy) cvn", [Name(True, "xyzzy")]),
        ("(xyzzy) cvx cvn", [Name(False, "xyzzy")]),
        # cvs
        ("123 (xyz) cvs", ["123"]),
        ("5 string dup 123 exch cvs", ["123\0\0", "123"]),
        ("/add load 5 string cvs", ["add"]),
        ("[1 2 3] 15 string cvs", ["--nostringval--"]),
        # forall
        ("(hello) {} forall", [104, 101, 108, 108, 111]),
        ("0 (hello) { add } forall", [532]),
        ("(ABCdef) { dup (a) 0 get ge {exit} if } forall", [65, 66, 67, 100]),
        # get
        ("(hello) 2 get", [108]),
        # getinterval
        ("(0123456789) 3 4 getinterval", ["3456"]),
        ("(0123456789) 6 4 getinterval", ["6789"]),
        ("(0123456789) 3 4 getinterval 1 2 getinterval", ["45"]),
        ("(0123456789) 3 0 getinterval", [""]),
        ("(0123456789) 3 0 getinterval 0 0 getinterval", [""]),
        ("(0123456789) 0 10 getinterval", ["0123456789"]),
        ("(0123456789) dup 3 4 getinterval 1 88 put", ["0123X56789"]),
        # length
        ("(hello) length", [5]),
        ("() length", [0]),
        ("/hello length", [5]),
        # put
        ("(hello) dup 2 88 put", ["heXlo"]),
        ("(hello) dup save exch 2 88 put restore", ["heXlo"]),  # strings don't restore
        # putinterval
        ("(0123456789) dup 3 (xyz) putinterval", ["012xyz6789"]),
        ("(0123) dup 0 (wxyz) putinterval", ["wxyz"]),
        ("(0123456789) dup 3 4 getinterval 1 (XYZ) putinterval", ["0123XYZ789"]),
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
        # cvn
        ("cvn", "stackunderflow"),
        ("123 cvn", "typecheck"),
        # cvs
        ("cvs", "stackunderflow"),
        ("() cvs", "stackunderflow"),
        ("123 123 cvs", "typecheck"),
        ("123 (ab) cvs", "rangecheck"),
        # forall
        ("(hello) 123 forall", "typecheck"),
        # get
        ("(hello) (a) get", "typecheck"),
        ("(hello) 10 get", "rangecheck"),
        ("(hello) -10 get", "rangecheck"),
        ("(hello) -1 get", "rangecheck"),
        # getinterval
        ("(hello) (a) 1 getinterval", "typecheck"),
        ("(hello) 1 (a) getinterval", "typecheck"),
        ("(hello) 1 10 getinterval", "rangecheck"),
        ("(hello) 0 6 getinterval", "rangecheck"),
        ("(hello) 10 1 getinterval", "rangecheck"),
        ("(hello) -1 1 getinterval", "rangecheck"),
        ("(hello) 1 -1 getinterval", "rangecheck"),
        # put
        ("(hello) (a) 123 put", "typecheck"),
        ("(hello) 2 (a) put", "typecheck"),
        ("(hello) 10 123 put", "rangecheck"),
        ("(hello) -10 123 put", "rangecheck"),
        # putinterval
        ("(hello) 4 123 putinterval", "typecheck"),
        ("(hello) 10 (a) putinterval", "rangecheck"),
        ("(hello) -1 (a) putinterval", "rangecheck"),
        ("(hello) 2 (hell) putinterval", "rangecheck"),
        # string
        ("string", "stackunderflow"),
        ("-1 string", "rangecheck"),
        ("3.4 string", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
