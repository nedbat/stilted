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

    def showpage(self):
        self.surface.finish()
        with open("page.svg", "wb") as page_svg:
            page_svg.write(self.svgio.getvalue())
