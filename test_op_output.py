"""Tests of output operators for stilted."""

import io

import pytest

from dtypes import MARK
from error import StiltedError
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack, output",
    [
        # =
        ("12345 =", [], "12345\n"),
        ("1234.5 =", [], "1234.5\n"),
        ("(hello) =", [], "hello\n"),
        ("(() =", [], "(\n"),
        ("/hello =", [], "hello\n"),
        ("/hello cvx =", [], "hello\n"),
        ("mark =", [], "--nostringval--\n"),
        ("null =", [], "--nostringval--\n"),
        ("true false = =", [], "false\ntrue\n"),
        ("systemdict =", [], "--nostringval--\n"),
        ("/add load =", [], "add\n"),
        ("{]} 0 get load =", [], "]\n"),
        ("save =", [], "--nostringval--\n"),
        ("[]=", [], "--nostringval--\n"),
        # ==
        ("12345 ==", [], "12345\n"),
        ("1234.5 ==", [], "1234.5\n"),
        ("(hello) ==", [], "(hello)\n"),
        ("(() ==", [], "(\\()\n"),
        ("(\\(\\)) ==", [], "(\\(\\))\n"),
        ("(first line\\nsecond) ==", [], "(first line\\nsecond)\n"),
        ("(octal: \\1) ==", [], "(octal: \\001)\n"),
        ("/hello ==", [], "/hello\n"),
        ("/hello cvx ==", [], "hello\n"),
        ("mark ==", [], "-mark-\n"),
        ("null ==", [], "null\n"),
        ("true false == ==", [], "false\ntrue\n"),
        ("systemdict ==", [], "-dict-\n"),
        ("/add load ==", [], "--add--\n"),
        ("{]} 0 get load ==", [], "--]--\n"),
        ("save ==", [], "-save-\n"),
        ("[] ==", [], "[]\n"),
        ("[1]==", [], "[1]\n"),
        ("[1 (a) null] ==", [], "[1 (a) null]\n"),
        ("{1 (a) null} ==", [], "{1 (a) null}\n"),
        # print
        ("(hello) print", [], "hello"),
        ("(hello) print (world) print", [], "helloworld"),
        ("() print", [], ""),
        ("(what\nnow) print", [], "what\nnow"),
        ("/hello print", [], "hello"),
        # pstack
        ("(hi) 123 mark pstack", ["hi", 123, MARK], "-mark-\n123\n(hi)\n"),
        # stack
        ("(hi) 123 mark stack", ["hi", 123, MARK], "--nostringval--\n123\nhi\n"),
    ],
)
def test_evaluate_with_output(text, stack, output):
    stdout = io.StringIO()
    engine = evaluate(text, stdout=stdout)
    compare_stacks(engine.ostack, stack)
    assert stdout.getvalue() == output


@pytest.mark.parametrize(
    "text, error",
    [
        # =
        ("=", "stackunderflow"),
        # ==
        ("==", "stackunderflow"),
        # print
        ("print", "stackunderflow"),
        ("123 print", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
