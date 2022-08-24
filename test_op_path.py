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
        # curveto
        ("0 0 moveto 101 202 303 404 505 606 curveto currentpoint", [505.0, 606.0]),
        # pathforall
        (
            # The basics work, and there isn't a moveto after a closepath.
            """
            10 20 moveto 30 40 lineto 1 2 3 4 5 6 curveto closepath
            {(M)} {(L)} {(C)} {(.)} pathforall
            """,
            [10.0, 20.0, "M", 30.0, 40.0, "L", 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, "C", "."],
        ),
        (
            # `exit` works.
            """
            10 20 moveto 30 40 lineto 1 2 3 4 5 6 curveto closepath
            {(M)} {(L)} { (!) exit} {(.)} pathforall
            """,
            [10.0, 20.0, "M", 30.0, 40.0, "L", 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, "!"],
        ),
        (
            # Coordinates are in the current coord system.
            "10 20 moveto 30 40 lineto 100 200 translate {} {} {} {} pathforall",
            [-90.0, -180.0, -70.0, -160.0],
        ),
        # rcurveto
        ("100 100 moveto 1 2 3 4 5 6 rcurveto currentpoint", [105.0, 106.0]),
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
        # pathforall
        ("pathforall", "stackunderflow"),
        ("{} pathforall", "stackunderflow"),
        ("{} {} pathforall", "stackunderflow"),
        ("{} {} {} pathforall", "stackunderflow"),
        ("12 {} {} {} pathforall", "typecheck"),
        ("{} 12 {} {} pathforall", "typecheck"),
        ("{} {} 12 {} pathforall", "typecheck"),
        ("{} {} {} 12 pathforall", "typecheck"),
        # rcurveto
        ("1 1 1 1 1 1 rcurveto", "nocurrentpoint"),
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


@pytest.mark.parametrize("op", ["curveto", "rcurveto"])
@pytest.mark.parametrize(
    "text, error",
    [
        ("@@", "stackunderflow"),
        ("1 @@", "stackunderflow"),
        ("1 1 @@", "stackunderflow"),
        ("1 1 1 @@", "stackunderflow"),
        ("1 1 1 1 @@", "stackunderflow"),
        ("1 1 1 1 1 @@", "stackunderflow"),
        ("(a) 1 1 1 1 1 @@", "typecheck"),
        ("1 (a) 1 1 1 1 @@", "typecheck"),
        ("1 1 (a) 1 1 1 @@", "typecheck"),
        ("1 1 1 (a) 1 1 @@", "typecheck"),
        ("1 1 1 1 (a) 1 @@", "typecheck"),
        ("1 1 1 1 1 (a) @@", "typecheck"),
    ],
)
def test_curveto_errors(op, text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text.replace("@@", op))
