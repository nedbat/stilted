"""Graphics state for Stilted."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

import io

import cairo

class Device:
    def __init__(self):
        self.width = 612
        self.height = 792
        self.svgio = io.BytesIO()
        self.surface = cairo.SVGSurface(self.svgio, self.width, self.height)
        self.surface.set_document_unit(cairo.SVGUnit.PT)
        self.ctx = cairo.Context(self.surface)
        self.ctx.set_line_width(1.0)
        self.default_matrix = self.ctx.get_matrix()

    def showpage(self):
        self.surface.finish()
        with open("page.svg", "wb") as page_svg:
            page_svg.write(self.svgio.getvalue())


@dataclass
class GstateExtras:
    """
    Extra info to save with the gstate.

    Most of the gstate is handled by PyCairo, but some information has to be
    handled separately.
    """

    # Was this gstate saved by `save` or `gsave`?
    from_save: bool

    # PyCairo doesn't restore the current point, so we do it ourselves.
    # https://github.com/pygobject/pycairo/issues/273
    cur_point: Tuple[float, float] | None

    @classmethod
    def from_ctx(cls, from_save: bool, ctx: cairo.Context) -> GstateExtras:
        """Construct a GstateExtras from a ctx."""
        if ctx.has_current_point():
            pt = ctx.get_current_point()
        else:
            pt = None
        return GstateExtras(from_save=from_save, cur_point=pt)

    def restore_to_ctx(self, ctx: cairo.Context) -> None:
        """Restore data from the Extras to the context."""
        if self.cur_point:
            ctx.move_to(*self.cur_point)
        else:
            ctx.new_path()
