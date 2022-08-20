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

        # Give subclasses a chance to do their things.
        self.surface: cairo.Surface
        self.make_surface()
        self.ctx = cairo.Context(self.surface)
        self.init_ctx()
        self.init_page()

        # Device-independent initialization.
        self.ctx.set_line_width(1.0)
        self.ctx.set_source_rgb(0, 0, 0)
        self.default_matrix = self.ctx.get_matrix()

    @classmethod
    def from_filename(cls, outfile):
        if outfile.endswith(".svg"):
            return SvgDevice(outfile)
        elif outfile.endswith(".png"):
            return PngDevice(outfile)
        else:
            raise Exception(f"Don't know how to write to {outfile!r}")

    def make_surface(self) -> None:
        raise NotImplementedError()

    def init_ctx(self) -> None:
        ...

    def init_page(self) -> None:
        ...

    def show_page(self) -> None:
        raise NotImplementedError()


class SvgDevice(Device):
    def make_surface(self) -> None:
        self.svgio = io.BytesIO()
        self.surface = cairo.SVGSurface(self.svgio, self.width, self.height)
        self.surface.set_document_unit(cairo.SVGUnit.PT)

    def init_ctx(self) -> None:
        self.ctx.translate(0, self.height)
        self.ctx.scale(1, -1)

    def show_page(self) -> None:
        self.surface.finish()
        with open(self.outfile, "wb") as page_svg:
            page_svg.write(self.svgio.getvalue())


class PngDevice(Device):
    def make_surface(self) -> None:
        pix_per_pt = 300 / 72
        self.surface: cairo.ImageSurface = cairo.ImageSurface(
            cairo.Format.RGB24,
            int(self.width * pix_per_pt),
            int(self.height * pix_per_pt),
        )

    def init_ctx(self) -> None:
        self.ctx.translate(0, self.surface.get_height())
        self.ctx.scale(1, -1)

    def init_page(self) -> None:
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.surface.get_width(), self.surface.get_height())
        self.ctx.fill()

    def show_page(self) -> None:
        self.surface.write_to_png(self.outfile)
        self.surface.finish()


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
