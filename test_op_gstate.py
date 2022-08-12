"""Tests of graphics state operators for Stilted."""

import pytest

from error import StiltedError
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # currentgray / setgray
        ("currentgray", [0.0]),
        (".75 setgray currentgray", [.75]),
        (".75 setgray gsave .5 setgray currentgray grestore currentgray", [.5, .75]),
        ("-.1 setgray currentgray", [0.0]),
        ("1.1 setgray currentgray", [1.0]),
        # currenthsbcolor / sethsbcolor
        (".1 .2 .3 setrgbcolor currenthsbcolor", [.5833333333333, .666666666, .3]),
        (".1 .2 .3 sethsbcolor currenthsbcolor", [.1, .2, .3]),
        (".1 .2 .3 sethsbcolor currentrgbcolor", [.3, .276, .24]),
        # currentlinecap / setlinecap
        ("currentlinecap", [0]),
        ("1 setlinecap currentlinecap", [1]),
        ("1 setlinecap gsave 2 setlinecap currentlinecap grestore currentlinecap", [2, 1]),
        # currentlinejoin / setlinejoin
        ("currentlinejoin", [0]),
        ("1 setlinejoin currentlinejoin", [1]),
        ("1 setlinejoin gsave 2 setlinejoin currentlinejoin grestore currentlinejoin", [2, 1]),
        # currentlinewidth / setlinewidth
        ("currentlinewidth", [1.0]),
        ("3.5 setlinewidth currentlinewidth", [3.5]),
        # currentmiterlimit / setmiterlimit
        ("currentmiterlimit", [10.0]),
        ("17.5 setmiterlimit currentmiterlimit", [17.5]),
        ("17.5 setmiterlimit gsave 35.25 setmiterlimit currentmiterlimit grestore currentmiterlimit", [35.25, 17.5]),
        # currentrgbcolor / setrgbcolor
        ("currentrgbcolor", [0.0, 0.0, 0.0]),
        (".1 .2 .3 setrgbcolor currentrgbcolor", [.1, .2, .3]),
        (".1 .2 .3 setrgbcolor currentgray", [.181]),
        (".1 .2 .3 setrgbcolor gsave .5 setgray currentrgbcolor grestore currentrgbcolor", [.5, .5, .5, .1, .2, .3]),
        ("-.5 .5 .5 setrgbcolor currentrgbcolor", [0., .5, .5]),
        ("1.5 .5 .5 setrgbcolor currentrgbcolor", [1., .5, .5]),
        (".5 -.5 .5 setrgbcolor currentrgbcolor", [.5, 0., .5]),
        (".5 1.5 .5 setrgbcolor currentrgbcolor", [.5, 1., .5]),
        (".5 .5 -.5 setrgbcolor currentrgbcolor", [.5, .5, 0.]),
        (".5 .5 1.5 setrgbcolor currentrgbcolor", [.5, .5, 1.]),
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
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # gsave
        ("gsave 10 10 moveto grestore currentpoint", "nocurrentpoint"),
        # setgray
        ("setgray", "stackunderflow"),
        ("(a) setgray", "typecheck"),
        # setlinecap
        ("setlinecap", "stackunderflow"),
        ("(a) setlinecap", "typecheck"),
        ("10 setlinecap", "rangecheck"),
        # setlinejoin
        ("setlinejoin", "stackunderflow"),
        ("(a) setlinejoin", "typecheck"),
        ("10 setlinejoin", "rangecheck"),
        # setlinewidth
        ("setlinewidth", "stackunderflow"),
        ("(a) setlinewidth", "typecheck"),
        # setmiterlimit
        ("setmiterlimit", "stackunderflow"),
        ("(a) setmiterlimit", "typecheck"),
        # sethsbcolor
        ("sethsbcolor", "stackunderflow"),
        (".5 sethsbcolor", "stackunderflow"),
        (".5 .5 sethsbcolor", "stackunderflow"),
        ("(a) .5 .5 sethsbcolor", "typecheck"),
        (".5 (a) .5 sethsbcolor", "typecheck"),
        (".5 .5 (a) sethsbcolor", "typecheck"),
        # setrgbcolor
        ("setrgbcolor", "stackunderflow"),
        (".5 setrgbcolor", "stackunderflow"),
        (".5 .5 setrgbcolor", "stackunderflow"),
        ("(a) .5 .5 setrgbcolor", "typecheck"),
        (".5 (a) .5 setrgbcolor", "typecheck"),
        (".5 .5 (a) setrgbcolor", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
