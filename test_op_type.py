"""Tests of type/attribute/conversion operators for Stilted."""

import pytest

from error import StiltedError
from evaluate import evaluate
from dtypes import Name
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # cvi
        ("-1.1 cvi", [-1]),
        ("3.14 cvi", [3]),
        ("(3.14) cvi", [3]),
        # cvlit
        ("{hello} cvlit xcheck", [False]),
        # cvn
        ("(xyzzy) cvn", [Name(True, "xyzzy")]),
        ("(xyzzy) cvx cvn", [Name(False, "xyzzy")]),
        # cvs
        ("123 (xyz) cvs", ["123"]),
        ("5 string dup 123 exch cvs", ["123\0\0", "123"]),
        ("/add load 5 string cvs", ["add"]),
        ("[1 2 3] 15 string cvs", ["--nostringval--"]),
        # cvx
        ("/Hello cvx xcheck", [True]),
        # type
        ("true type", [Name(False, "booleantype")]),
        ("123 type", [Name(False, "integertype")]),
        ("mark type", [Name(False, "marktype")]),
        ("/Name type", [Name(False, "nametype")]),
        ("null type", [Name(False, "nulltype")]),
        ("12.3 type", [Name(False, "realtype")]),
        ("(hello) type", [Name(False, "stringtype")]),
        ("systemdict type", [Name(False, "dicttype")]),
        ("/add load type", [Name(False, "operatortype")]),
        ("save type", [Name(False, "savetype")]),
        # xcheck
        ("/Hello xcheck", [False]),
        ("{hello} xcheck", [True]),
        ("123 xcheck", [False]),
        ("mark xcheck", [False]),
        ("null xcheck", [False]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # cvi
        ("cvi", "stackunderflow"),
        ("[] cvi", "typecheck"),
        ("(xyz) cvi", "undefinedresult"), # gs and xpost disagree on this result.
        # cvlit
        ("cvlit", "stackunderflow"),
        # cvn
        ("cvn", "stackunderflow"),
        ("123 cvn", "typecheck"),
        # cvs
        ("cvs", "stackunderflow"),
        ("() cvs", "stackunderflow"),
        ("123 123 cvs", "typecheck"),
        ("123 (ab) cvs", "rangecheck"),
        # cvx
        ("cvx", "stackunderflow"),
        # type
        ("type", "stackunderflow"),
        # xcheck
        ("xcheck", "stackunderflow"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
