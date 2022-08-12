"""Tests of path construction operators for Stilted."""

import pytest

from error import StiltedError
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # arc
        ("0 0 100 0 90 arc currentpoint", [0.0, 100.0]),
        # arcn
        ("0 0 100 90 0 arcn currentpoint", [100.0, 0.0]),
        # closepath
        ("1 2 moveto 1 3 lineto 3 1 lineto closepath currentpoint", [1.0, 2.0]),
        # currentpoint
        ("101 202 moveto currentpoint", [101.0, 202.0]),
        ("101 202 moveto 303 404 moveto currentpoint", [303.0, 404.0]),
        ("101 202 moveto 303 404 lineto currentpoint", [303.0, 404.0]),
        # rlineto
        ("1 2 moveto 10 20 rlineto currentpoint", [11.0, 22.0]),
        # rmoveto
        ("1 2 moveto 10 20 rmoveto currentpoint", [11.0, 22.0]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # currentpoint
        ("currentpoint", "nocurrentpoint"),
        ("10 10 moveto 20 20 lineto stroke currentpoint", "nocurrentpoint"),
        # lineto
        ("lineto", "stackunderflow"),
        ("1 lineto", "stackunderflow"),
        ("(a) 1 lineto", "typecheck"),
        ("1 (a) lineto", "typecheck"),
        ("1 1 lineto", "nocurrentpoint"),
        # moveto
        ("moveto", "stackunderflow"),
        ("1 moveto", "stackunderflow"),
        ("(a) 1 moveto", "typecheck"),
        ("1 (a) moveto", "typecheck"),
        # newpath
        ("10 10 moveto newpath currentpoint", "nocurrentpoint"),
        # rlineto
        ("rlineto", "stackunderflow"),
        ("1 rlineto", "stackunderflow"),
        ("(a) 1 rlineto", "typecheck"),
        ("1 (a) rlineto", "typecheck"),
        ("1 1 rlineto", "nocurrentpoint"),
        # rmoveto
        ("rmoveto", "stackunderflow"),
        ("1 rmoveto", "stackunderflow"),
        ("(a) 1 rmoveto", "typecheck"),
        ("1 (a) rmoveto", "typecheck"),
        ("1 1 rmoveto", "nocurrentpoint"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)


@pytest.mark.parametrize("op", ["arc", "arcn"])
@pytest.mark.parametrize(
    "text, error",
    [
        ("@@", "stackunderflow"),
        ("1 @@", "stackunderflow"),
        ("1 1 @@", "stackunderflow"),
        ("1 1 1 @@", "stackunderflow"),
        ("1 1 1 1 @@", "stackunderflow"),
        ("(a) 1 1 1 1 @@", "typecheck"),
        ("1 (a) 1 1 1 @@", "typecheck"),
        ("1 1 (a) 1 1 @@", "typecheck"),
        ("1 1 1 (a) 1 @@", "typecheck"),
        ("1 1 1 1 (a) @@", "typecheck"),
    ],
)
def test_arc_errors(op, text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text.replace("@@", op))
