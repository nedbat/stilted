"""Errors that stilted can raise."""

class Tilted(Exception):
    def __init__(self, errname):
        self.errname = errname
