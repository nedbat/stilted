"""Tests of graphics state operators for Stilted."""

import pytest

from error import StiltedError
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # currentlinewidth
        ("currentlinewidth", [1.0]),
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
        # setlinewidth
        ("3.5 setlinewidth currentlinewidth", [3.5]),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # gsave
        ("gsave 10 10 moveto grestore currentpoint", "nocurrentpoint"),
        # setlinewidth
        ("setlinewidth", "stackunderflow"),
        ("(a) setlinewidth", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
