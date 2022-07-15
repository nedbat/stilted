"""Tests of stack operators for stilted."""

import pytest

from error import Tilted
from evaluate import evaluate
from pstypes import MARK


@pytest.mark.parametrize(
    "text, stack",
    [
        # clear
        ("1 2 3 clear", []),
        # cleartomark
        ("1 [ 2 3 cleartomark", [1]),
        # copy
        ("(a) (b) (c) 2 copy", ["a", "b", "c", "b", "c"]),
        ("(a) (b) (c) 0 copy", ["a", "b", "c"]),
        # count
        ("count", [0]),
        ("1 2 3 count", [1, 2, 3, 3]),
        # counttomark
        ("mark 1 2 3 counttomark", [MARK, 1, 2, 3, 3]),
        ("mark counttomark", [MARK, 0]),
        # dup
        ("1 123 dup", [1, 123, 123]),
        # exch
        ("1 123 456 exch", [1, 456, 123]),
        # index
        ("(a) (b) (c) (d) 0 index", ["a", "b", "c", "d", "d"]),
        ("(a) (b) (c) (d) 3 index", ["a", "b", "c", "d", "a"]),
        # mark
        ("1 mark", [1, MARK]),
        ("1 [", [1, MARK]),
        # pop
        ("1 123 pop", [1]),
        # roll
        ("(a) (b) (c) 3 -1 roll", ["b", "c", "a"]),
        ("(a) (b) (c) 3 1 roll", ["c", "a", "b"]),
        ("(a) (b) (c) 3 0 roll", ["a", "b", "c"]),
        # def
        ("1 /hello (there) def 2 hello", [1, 2, "there"]),
    ],
)
def test_evaluate(text, stack):
    assert evaluate(text).ostack == stack


@pytest.mark.parametrize(
    "text, error",
    [
        # cleartomark
        ("1 2 3 cleartomark", "unmatchedmark"),
        # copy
        ("copy", "stackunderflow"),
        ("(a) (b) 3 copy", "stackunderflow"),
        # counttomark
        ("1 2 3 counttomark", "unmatchedmark"),
        # dup
        ("dup", "stackunderflow"),
        # exch
        ("exch", "stackunderflow"),
        ("1 exch", "stackunderflow"),
        # pop
        ("pop", "stackunderflow"),
        # roll
        ("1 2 3 4 1 roll", "stackunderflow"),
        ("roll", "stackunderflow"),
        ("1 0 roll", "stackunderflow"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(Tilted, match=error):
        evaluate(text)
