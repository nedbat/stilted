"""Errors that Stilted can raise."""

class Tilted(Exception):
    """Any stilted exception."""

    def __init__(self, errname: str) -> None:
        super().__init__(errname)
        self.errname = errname
