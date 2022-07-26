"""Tests of collections operators for stilted."""

import pytest

from error import StiltedError
from evaluate import evaluate


@pytest.mark.parametrize(
    "text, error",
    [
        # get
        ("get", "stackunderflow"),
        ("/foo get", "stackunderflow"),
        ("123 /foo get", "typecheck"),
        # getinterval
        ("getinterval", "stackunderflow"),
        ("1 getinterval", "stackunderflow"),
        ("1 2 getinterval", "stackunderflow"),
        ("3.1415 1 2 getinterval", "typecheck"),
        # length
        ("length", "stackunderflow"),
        ("213 length", "typecheck"),
        # put
        ("put", "stackunderflow"),
        ("12 put", "stackunderflow"),
        ("/foo 12 put", "stackunderflow"),
        ("123 /foo 12 put", "typecheck"),
        # putinterval
        ("putinterval", "stackunderflow"),
        ("12 putinterval", "stackunderflow"),
        ("/foo 12 putinterval", "stackunderflow"),
        ("123 /foo 12 putinterval", "typecheck"),
        ("123 12 /foo putinterval", "typecheck"),
    ],
)
def test_evaluate_error(text, error):
    with pytest.raises(StiltedError, match=error):
        evaluate(text)
