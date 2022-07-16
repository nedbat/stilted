"""Errors that stilted can raise."""

class Tilted(Exception):
    """Any stilted exception."""

    def __init__(self, errname):
        super().__init__(errname)
        self.errname = errname
