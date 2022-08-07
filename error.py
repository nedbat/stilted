"""Errors that Stilted can raise."""

class Tilted(Exception):
    """A Stilted exception that will be handled by Stilted."""

    def __init__(self, errname: str, info: str|None=None) -> None:
        super().__init__(errname)
        assert errname in ERROR_NAMES
        self.errname = errname
        self.info = info


class FinalTilt(Exception):
    """An exception to raise to the Python wrapper."""


# These are the official error names, though Stilted can't raise all of them.

ERROR_NAMES = {
    "VMerror",
    "configurationerror",
    "dictfull",
    "dictstackoverflow",
    "dictstackunderflow",
    "execstackoverflow",
    "handleerror",
    "interrupt",
    "invalidaccess",
    "invalidcontext",
    "invalidexit",
    "invalidfileaccess",
    "invalidfont",
    "invalidrestore",
    "ioerror",
    "limitcheck",
    "nocurrentpoint",
    "rangecheck",
    "stackoverflow",
    "stackunderflow",
    "syntaxerror",
    "timeout",
    "typecheck",
    "undefined",
    "undefinedfilename",
    "undefinedresource",
    "undefinedresult",
    "unmatchedmark",
    "unregistered",
}
