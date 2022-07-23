"""Tests of output operators for stilted."""

import io

import pytest

from dtypes import MARK
from error import Tilted
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
        ("true false = =", [], "false\ntrue\n"),
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
        ("true false == ==", [], "false\ntrue\n"),
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
    estate = evaluate(text, stdout=stdout)
    compare_stacks(estate.ostack, stack)
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
    with pytest.raises(Tilted, match=error):
        evaluate(text)
