"""Output devices for Stilted."""

from __future__ import annotations
import io

import cairo

class Device:

    def __init__(self, outfile) -> None:
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
    def from_filename(cls, outfile) -> Device:
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
