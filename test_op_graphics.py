"""Tests of graphics operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # currentlinewidth
        ("currentlinewidth", [1.0]),
        # currentpoint
        ("101 202 moveto currentpoint", [101.0, 202.0]),
        ("101 202 moveto 303 404 moveto currentpoint", [303.0, 404.0]),
        ("101 202 moveto 303 404 lineto currentpoint", [303.0, 404.0]),
        # grestore
        ("grestore grestore grestore", []),
        # grestoreall
        ("grestoreall grestoreall grestoreall", []),
        ("101 202 moveto save pop 3 4 moveto gsave 5 6 moveto gsave grestoreall currentpoint", [101.0, 202.0]),
        # gsave/grestore
        ("101 202 moveto gsave 303 404 moveto grestore currentpoint", [101.0, 202.0]),
        ("1 2 moveto gsave 3 4 moveto save pop 5 6 moveto grestore grestore grestore currentpoint", [3.0, 4.0]),
        ("1 2 moveto gsave 3 4 moveto save 5 6 moveto gsave 7 8 moveto gsave restore currentpoint", [3.0, 4.0]),
        ("2.5 setlinewidth gsave 3.5 setlinewidth grestore currentlinewidth", [2.5]),
        # rlineto
        ("1 2 moveto 10 20 rlineto currentpoint", [11.0, 22.0]),
        # rmoveto
        ("1 2 moveto 10 20 rmoveto currentpoint", [11.0, 22.0]),
        # setlinewidth
        ("3.5 setlinewidth currentlinewidth", [3.5]),
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
        # gsave
        ("gsave 10 10 moveto grestore currentpoint", "nocurrentpoint"),
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
        # setlinewidth
        ("setlinewidth", "stackunderflow"),
        ("(a) setlinewidth", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
