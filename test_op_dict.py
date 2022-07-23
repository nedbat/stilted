"""Tests of dict operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from dtypes import Name
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # begin
        ("10 dict dup begin /foo 17 def end /foo get /foo where", [17, False]),
        # countdictstack
        ("countdictstack", [2]),
        ("10 dict begin countdictstack", [3]),
        # dict
        ("10 dict type", [Name(False, "dicttype")]),
        ("10 dict dup /foo 23 put /foo get", [23]),
        # get
        ("systemdict /add get type", [Name(False, "operatortype")]),
        # load
        ("/add load type", [Name(False, "operatortype")]),
        # known
        ("systemdict /add known", [True]),
        ("systemdict /xyzzy known", [False]),
        # put
        ("userdict /foo 17 put foo", [17]),
        ("userdict /foo 17 put userdict /foo 23 put foo", [23]),
        # systemdict
        ("systemdict type", [Name(False, "dicttype")]),
        # userdict
        ("userdict type", [Name(False, "dicttype")]),
        ("userdict /xyzzy known", [False]),
        ("/xyzzy 21 def userdict /xyzzy known", [True]),
        # where
        ("/add where { /sub get type } { (buh) } ifelse", [Name(False, "operatortype")]),
        ("/xyzzy where {(buh)} {(nope)} ifelse", ["nope"]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # begin
        ("begin", "stackunderflow"),
        ("123 begin", "typecheck"),
        # dict
        ("dict", "stackunderflow"),
        ("-1 dict", "rangecheck"),
        ("() dict", "typecheck"),
        # end
        ("end", "dictstackunderflow"),
        ("10 dict begin end end", "dictstackunderflow"),
        # get
        ("get", "stackunderflow"),
        ("/foo get", "stackunderflow"),
        ("123 /foo get", "typecheck"),
        ("systemdict 123 get", "typecheck"),
        ("systemdict /xyzzy get", "undefined: xyzzy"),
        # load
        ("load", "stackunderflow"),
        ("123 load", "typecheck"),
        ("/xyzzy load", "undefined: xyzzy"),
        # known
        ("known", "stackunderflow"),
        ("/foo known", "stackunderflow"),
        ("123 /foo known", "typecheck"),
        ("systemdict 123 known", "typecheck"),
        # put
        ("put", "stackunderflow"),
        ("12 put", "stackunderflow"),
        ("/foo 12 put", "stackunderflow"),
        ("123 /foo 12 put", "typecheck"),
        ("userdict true 12 put", "typecheck"),
        # where
        ("where", "stackunderflow"),
        ("23 where", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
