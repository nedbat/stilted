"""Tests of font operators for Stilted."""

import pytest

from error import StiltedError
from evaluate import evaluate
from test_helpers import compare_stacks


@pytest.mark.parametrize(
    "text, stack",
    [
        # charpath
        (
            """
            /sans findfont 1000 scalefont setfont
            0 0 moveto (Hello) false charpath
            {/my exch def /mx exch def} { clear } { clear } { clear } pathforall
            my 0 eq
            (Hello) stringwidth
            0 eq exch
            mx sub abs .001 lt
            """,
            [True, True, True],
        ),
        # findfont
        ("/f /Helvetica findfont def [/FontType /FontName] {f exch get} forall", "1 /Helvetica"),
        # multiple
        (
            """
            /f /sans findfont def /s (Hello) def
            f 100 scalefont setfont (Hello) stringwidth 0 ne {xyzzy} if
            f 200 scalefont setfont (Hello) stringwidth 0 ne {xyzzy} if
            2 div sub
            """,
            [0.0]
        ),
        ("/sans findfont 100 scalefont setfont () stringwidth", [0.0, 0.0]),
        (
            """
            /sans findfont 1000 scalefont setfont 0 0 moveto (Hello) show
            currentpoint 0 ne {xyzzy} if
            (Hello) stringwidth 0 ne {xyzzy} if
            sub
            """,
            [0.0]
        ),
        (
            """
            /sans findfont setfont currentfont /FontName get
            gsave
            /serif findfont setfont currentfont /FontName get
            grestore
            currentfont /FontName get
            """,
            "/sans /serif /sans",
        ),
    ],
)
def test_evaluate(text, stack):
    compare_stacks(evaluate(text).ostack, stack)


@pytest.mark.parametrize(
    "text, error",
    [
        # charpath
        ("charpath", "stackunderflow"),
        ("true charpath", "stackunderflow"),
        ("(a) false charpath", "nocurrentpoint"),
        # findfont
        ("findfont", "stackunderflow"),
        ("1 findfont", "typecheck"),
        # scalefont
        ("scalefont", "stackunderflow"),
        ("1 scalefont", "stackunderflow"),
        ("(a) 1 scalefont", "typecheck"),
        ("/sans findfont (a) scalefont", "typecheck"),
        # setfont
        ("setfont", "stackunderflow"),
        ("(a) setfont", "typecheck"),
        # show
        ("show", "stackunderflow"),
        ("1 show", "typecheck"),
        ("(a) show", "nocurrentpoint"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
