"""Graphics state for Stilted."""

from __future__ import annotations
import dataclasses
from dataclasses import dataclass
from typing import TYPE_CHECKING

import io

import cairo

from dtypes import Object

if TYPE_CHECKING:   # pragma: no cover
    from evaluate import Engine

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
    Extra information needed beyond the Cairo graphics state.

    Most current graphics state is in the Cairo state
    """
    # The font dict.
    font_dict: dict[str, Object]

    def copy(self) -> GstateExtras:
        """Make a copy of this object."""
        return dataclasses.replace(self)


@dataclass
class SavedGstate:
    """
    Graphics state for gsave/grestore

    PyCairo can save/restore its graphics state, but we need more control, so
    this is the full explicit graphics state.

    PyCairo doesn't restore the current path, so we do it ourselves.
    https://github.com/pygobject/pycairo/issues/273

    """

    # Was this gstate saved by `save` or `gsave`?
    from_save: bool

    # The components of the PostScript graphics state.
    ctm: cairo.Matrix
    position: tuple[float, float]
    cur_path: cairo.Path
    rgba: tuple[float, float, float, float]
    line_width: float
    line_cap: cairo.LineCap
    line_join: cairo.LineJoin
    miter_limit: float
    dash: tuple[list[float], float]

    # The GstateExtras.
    gextra: GstateExtras

    @classmethod
    def from_ctx(cls, from_save: bool, ctx: cairo.Context, extra=GstateExtras) -> SavedGstate:
        """Construct a SavedGstate from a ctx."""
        return cls(
            from_save=from_save,
            ctm=ctx.get_matrix(),
            position=ctx.get_current_point(),
            cur_path=ctx.copy_path(),
            rgba=ctx.get_source().get_rgba(),   # type: ignore
            line_width=ctx.get_line_width(),
            line_cap=ctx.get_line_cap(),
            line_join=ctx.get_line_join(),
            miter_limit=ctx.get_miter_limit(),
            dash=ctx.get_dash(),
            gextra=extra.copy(),
        )

    def restore_to_ctx(self, ctx: cairo.Context, engine: Engine) -> None:
        """Restore data from the SavedGstate to the context."""
        ctx.set_matrix(self.ctm)
        ctx.new_path()
        ctx.append_path(self.cur_path)
        ctx.set_source_rgba(*self.rgba)
        ctx.set_line_width(self.line_width)
        ctx.set_line_cap(self.line_cap)
        ctx.set_line_join(self.line_join)
        ctx.set_miter_limit(self.miter_limit)
        ctx.set_dash(*self.dash)
        engine.gextra = self.gextra
        engine.set_font(self.gextra.font_dict)
