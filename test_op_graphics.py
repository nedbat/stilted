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
        ("3.5 setlinewidth currentlinewidth", [3.5]),
        # currentpoint
        ("101 202 moveto currentpoint", [101.0, 202.0]),
        ("101 202 moveto 303 404 lineto currentpoint", [303.0, 404.0]),
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
        # setlinewidth
        ("setlinewidth", "stackunderflow"),
        ("(a) setlinewidth", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
