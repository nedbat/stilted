"""Built-in font operators for Stilted."""

import cairo

from cairo_util import array_to_cmatrix, cmatrix_to_array, has_current_point
from dtypes import Boolean, Dict, Name, Number, String, from_py
from error import Tilted
from evaluate import operator, Engine

@operator
def charpath(engine: Engine) -> None:
    stroke_or_fill = engine.opop(Boolean)
    text = engine.opop(String)
    if stroke_or_fill.value:
        raise Tilted("undefinedresult")
    has_current_point(engine)
    engine.gctx.text_path(text.str_value)

@operator
def currentfont(engine: Engine) -> None:
    engine.opush(engine.new_dict(value=engine.gextra.font_dict))

@operator
def findfont(engine: Engine) -> None:
    name = engine.opop(Name)
    arr = engine.new_array(n=6)
    cmatrix_to_array(cairo.Matrix(), arr)
    font_dict = {
        "FontMatrix": arr,
        "FontName": name,
        "FontType": from_py(1),
    }
    engine.opush(engine.new_dict(value=font_dict))

@operator
def scalefont(engine: Engine) -> None:
    scale = engine.opop(Number).value
    font_dict = engine.opop(Dict).value
    mtx = array_to_cmatrix(font_dict["FontMatrix"])
    mtx.scale(scale, scale)
    arr = engine.new_array(n=6)
    cmatrix_to_array(mtx, arr)
    font_dict_scaled = dict(font_dict)
    font_dict_scaled["FontMatrix"] = arr
    engine.opush(engine.new_dict(value=font_dict_scaled))

@operator
def setfont(engine: Engine) -> None:
    font_dict = engine.opop(Dict).value
    engine.set_font(font_dict)

@operator
def show(engine: Engine) -> None:
    text = engine.opop(String)
    has_current_point(engine)
    engine.gctx.show_text(text.str_value)

@operator
def stringwidth(engine: Engine) -> None:
    text = engine.opop(String)
    extents = engine.gctx.text_extents(text.str_value)
    engine.opush(from_py(extents.x_advance), from_py(extents.y_advance))
