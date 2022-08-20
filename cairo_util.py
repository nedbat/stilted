"""Cairo utilities for Stilted."""

import cairo

from dtypes import from_py, Array
from error import Tilted
from evaluate import Engine


def has_current_point(engine: Engine) -> None:
    """There must be a current point, or raise nocurrentpoint."""
    if not engine.gctx.has_current_point():
        raise Tilted("nocurrentpoint")


def cmatrix_to_array(mtx: cairo.Matrix, arr: Array):
    """Assign mtx into arr."""
    lmtx = list(mtx) # type: ignore
    for i in range(6):
        arr[i] = from_py(lmtx[i])


def array_to_cmatrix(arr) -> cairo.Matrix:
    """Convert an Array into a Matrix."""
    return cairo.Matrix(*map(lambda o: o.value, arr))
