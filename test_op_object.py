"""Tests of object model operators for stilted."""

import pytest

from error import Tilted
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
        # cvx
        ("cvx", "stackunderflow"),
        # type
        ("type", "stackunderflow"),
        # xcheck
        ("xcheck", "stackunderflow"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
