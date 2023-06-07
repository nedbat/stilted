"""Output devices for Stilted."""

from __future__ import annotations
import io
import itertools

import cairo

class Device:

    def __init__(self, outfile, size=None) -> None:
        self.outfile = outfile
        self.width, self.height = size or (612, 792)

        # Give subclasses a chance to do their things.
        self.ctx: cairo.Context
        self.make_ctx()

        # Device-independent initialization.
        self.ctx.set_line_width(1.0)
        self.ctx.set_source_rgb(0, 0, 0)
        self.default_matrix = self.ctx.get_matrix()

        self.page_nums = itertools.count(start=1)

    @classmethod
    def from_filename(cls, outfile, size=None) -> Device:
        if outfile.endswith(".svg"):
            return SvgDevice(outfile, size)
        elif outfile.endswith(".png"):
            return PngDevice(outfile, size)
        else:
            raise Exception(f"Don't know how to write to {outfile!r}")

    def make_ctx(self) -> None:
        raise NotImplementedError()

    def show_page(self) -> None:
        raise NotImplementedError()

    def page_file_name(self) -> str:
        if "%" in self.outfile:
            return self.outfile % (next(self.page_nums))
        else:
            return self.outfile


class SvgDevice(Device):
    def make_ctx(self) -> None:
        self.svgio = io.BytesIO()
        self.surface = cairo.SVGSurface(self.svgio, self.width, self.height)
        self.surface.set_document_unit(cairo.SVGUnit.PT)
        self.ctx = cairo.Context(self.surface)
        self.ctx.translate(0, self.height)
        self.ctx.scale(1, -1)

    def show_page(self) -> None:
        self.surface.finish()
        with open(self.page_file_name(), "wb") as page_svg:
            page_svg.write(self.svgio.getvalue())
        self.make_ctx()


class PngDevice(Device):
    def make_ctx(self) -> None:
        pix_per_pt = 300 / 72
        self.surface: cairo.ImageSurface = cairo.ImageSurface(
            cairo.Format.RGB24,
            int(self.width * pix_per_pt),
            int(self.height * pix_per_pt),
        )

        self.ctx = cairo.Context(self.surface)
        self.ctx.translate(0, self.surface.get_height())
        self.ctx.scale(1, -1)

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.surface.get_width(), self.surface.get_height())
        self.ctx.fill()

    def show_page(self) -> None:
        self.surface.write_to_png(self.page_file_name())
        self.surface.finish()
        self.make_ctx()
