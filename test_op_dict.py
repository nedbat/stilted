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
        # currentdict
        ("10 dict begin /foo 17 def currentdict /foo known", [True]),
        # def
        ("1 /hello (there) def 2 hello", [1, 2, "there"]),
        # dict
        ("10 dict type", [Name(False, "dicttype")]),
        ("10 dict dup /foo 23 put /foo get", [23]),
        # get
        ("systemdict /add get type", [Name(False, "operatortype")]),
        # length
        ("10 dict length", [0]),
        ("10 dict begin /foo 10 def /bar 11 def currentdict length", [2]),
        # load
        ("/add load type", [Name(False, "operatortype")]),
        # known
        ("systemdict /add known", [True]),
        ("systemdict /xyzzy known", [False]),
        # put
        ("userdict /foo 17 put foo", [17]),
        ("userdict /foo 17 put userdict /foo 23 put foo", [23]),
        # store
        ("10 dict begin /foo 17 def 10 dict begin /foo 23 store end foo", [23]),
        ("10 dict begin 10 dict begin /foo 23 store end /foo where", [False]),
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
        # def
        ("def", "stackunderflow"),
        ("12 def", "stackunderflow"),
        ("123 45 def", "typecheck"),
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
        # length
        ("length", "stackunderflow"),
        ("213 length", "typecheck"),
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
        # store
        ("store", "stackunderflow"),
        ("12 store", "stackunderflow"),
        ("12 34 store", "typecheck"),
        # where
        ("where", "stackunderflow"),
        ("23 where", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
