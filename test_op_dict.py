"""Tests of dict operators for stilted."""

import pytest

from error import StiltedError
from evaluate import evaluate
from dtypes import Name
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # begin
        ("10 dict dup begin /foo 17 def end /foo get /foo where", [17, False]),
        # cleardictstack
        ("cleardictstack countdictstack", [2]),
        ("10 dict begin cleardictstack countdictstack", [2]),
        # copy
        ("""
            /d1 10 dict def /d2 10 dict def
            d1 begin
            /foo 123 def
            /bar 345 def
            end
            save
            d1 d2 copy length       % the length of the copy is 2
            d2 /foo get
            d2 /bar get
            4 -1 roll restore       % restore to before the copy
            d2 length               % the length is now 0
            """,
            [2, 123, 345, 0],
        ),
        # countdictstack
        ("countdictstack", [2]),
        ("10 dict begin countdictstack", [3]),
        # currentdict
        ("10 dict begin /foo 17 def currentdict /foo known", [True]),
        # def
        ("1 /hello (there) def 2 hello", [1, 2, "there"]),
        ("1 (hello) (there) def 2 hello", [1, 2, "there"]),
        # dict
        ("10 dict type", [Name(False, "dicttype")]),
        ("10 dict dup /foo 23 put /foo get", [23]),
        # forall
        ("""
            /d 2 dict def
            d /abc 123 put
            d /xyz (test) put
            d { 1 } forall
            """,
            [Name(True, "abc"), 123, 1, Name(True, "xyz"), "test", 1],
        ),
        ("10 dict {(what)} forall", []),
        ("""
            /d 2 dict def
            d /abc 123 put
            d /xyz (test) put
            d { dup 123 eq { exit } if } forall
            """,
            [Name(True, "abc"), 123],
        ),
        # get
        ("systemdict /add get type", [Name(False, "operatortype")]),
        # known
        ("systemdict /add known", [True]),
        ("systemdict (add) known", [True]),
        ("systemdict /xyzzy known", [False]),
        # length
        ("10 dict length", [0]),
        ("10 dict begin /foo 10 def /bar 11 def currentdict length", [2]),
        # load
        ("/add load type", [Name(False, "operatortype")]),
        ("(add) load type", [Name(False, "operatortype")]),
        # maxlength
        ("10 dict dup maxlength exch length gt", [True]),
        # put
        ("userdict /foo 17 put foo", [17]),
        ("userdict (foo) 17 put foo", [17]),
        ("userdict /foo 17 put userdict /foo 23 put foo", [23]),
        # store
        ("10 dict begin /foo 17 def 10 dict begin /foo 23 store end foo", [23]),
        ("10 dict begin (foo) 17 def 10 dict begin (foo) 23 store end foo", [23]),
        ("10 dict begin 10 dict begin /foo 23 store end /foo where", [False]),
        # systemdict
        ("systemdict type", [Name(False, "dicttype")]),
        # userdict
        ("userdict type", [Name(False, "dicttype")]),
        ("userdict /xyzzy known", [False]),
        ("/xyzzy 21 def userdict /xyzzy known", [True]),
        # where
        ("/add where { /sub get type } { (buh) } ifelse", [Name(False, "operatortype")]),
        ("(add) where { (sub) get type } { (buh) } ifelse", [Name(False, "operatortype")]),
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
        # copy
        ("10 dict 3.5 copy", "typecheck"),
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
        ("systemdict 123 get", "typecheck"),
        ("systemdict /xyzzy get", "undefined"),
        # known
        ("known", "stackunderflow"),
        ("/foo known", "stackunderflow"),
        ("123 /foo known", "typecheck"),
        ("systemdict 123 known", "typecheck"),
        # load
        ("load", "stackunderflow"),
        ("123 load", "typecheck"),
        ("/xyzzy load", "undefined"),
        # maxlength
        ("maxlength", "stackunderflow"),
        ("213 maxlength", "typecheck"),
        # put
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
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
