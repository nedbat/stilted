"""Utilities for Stilted."""

import math

from error import Tilted

def rangecheck(lo: float, val: float, hi: float | None=None) -> None:
    """Check that `lo <= val` and `val <= hi`."""
    if not (lo <= val):
        raise Tilted("rangecheck", f"need {lo} <= {val}")
    if hi is not None:
        if not (val <= hi):
            raise Tilted("rangecheck", f"need {val} <= {hi}")


def clamp(lo: float, val: float, hi: float) -> float:
    """If `val` is outside `lo`..`hi`, set it to `lo` or `hi`."""
    if val < lo:
        return lo
    elif val > hi:
        return hi
    else:
        return val


def deg_to_rad(degrees: float) -> float:
    """Convert degrees to radians."""
    return math.pi * degrees / 180
