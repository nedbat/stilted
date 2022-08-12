"""Graphics state for Stilted."""

from __future__ import annotations
from dataclasses import dataclass

import io

import cairo

class Device:
    def __init__(self, outfile):
        self.outfile = outfile
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
        with open(self.outfile, "wb") as page_svg:
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

    # PyCairo doesn't restore the current path, so we do it ourselves.
    # https://github.com/pygobject/pycairo/issues/273
    cur_path: cairo.Path

    @classmethod
    def from_ctx(cls, from_save: bool, ctx: cairo.Context) -> GstateExtras:
        """Construct a GstateExtras from a ctx."""
        return GstateExtras(from_save=from_save, cur_path=ctx.copy_path())

    def restore_to_ctx(self, ctx: cairo.Context) -> None:
        """Restore data from the Extras to the context."""
        ctx.new_path()
        ctx.append_path(self.cur_path)
