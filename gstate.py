"""Graphics state for Stilted."""

from __future__ import annotations
import dataclasses
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import cairo

from dtypes import Object

if TYPE_CHECKING:   # pragma: no cover
    from evaluate import Engine

@dataclass
class GstateExtras:
    """
    Extra information needed beyond the Cairo graphics state.

    Most current graphics state is in the Cairo state.
    """
    # The font dict.
    font_dict: dict[str, Object] = field(default_factory=dict)

    # Really esoteric: Cairo adds a moveto after a closepath. I don't want to
    # see that moveto when doing pathforall.  But it doesn't add a moveto
    # when the path is from charpath. This is a list of begin/end pairs of the
    # path segments from charpath, so we can properly skip the synthetic
    # movetos.
    charpath_segments: list[tuple[int, int]] = field(default_factory=list)

    # Cairo isn't good about giving back the clip path, so we store all the
    # paths that have been clipped to. When we need to restore the clip path,
    # we can re-create it by clipping to each of them in turn.
    clip_stack: list[
        tuple[
            cairo.FillRule,
            cairo.Matrix,
            cairo.Path,
            ]
        ] = field(default_factory=list)

    def copy(self) -> GstateExtras:
        """Make a copy of this object."""
        return dataclasses.replace(
            self,
            charpath_segments=list(self.charpath_segments),
            clip_stack=list(self.clip_stack),
            )


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
        ctx.reset_clip()
        for fill_rule, mtx, path in self.gextra.clip_stack:
            ctx.set_matrix(mtx)
            ctx.new_path()
            ctx.append_path(path)
            ctx.set_fill_rule(fill_rule)
            ctx.clip()

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
