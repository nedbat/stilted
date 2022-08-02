"""Main program for CLI usage of Stilted."""

import argparse
import pathlib
import sys
from typing import Callable

from error import Tilted
from evaluate import Engine


def main(argv: list[str], input_fn: Callable[[str], str]=input) -> int:
    parser = argparse.ArgumentParser(
        description="Stilted, a tiny PostScript implementation.",
        usage="cli.py [option] ... [-c CODE | file] [arg] ...",
    )
    parser.add_argument(
        "-c", dest="code",
        help="Code to run immediately",
    )
    parser.add_argument(
        "-i", dest="interactive", action="store_true",
        help="Run an interactive prompt when code is finished",
    )
    parser.add_argument("args", nargs="*")

    args = parser.parse_args(argv)

    engine = Engine()

    code = None
    if args.code:
        code = args.code
    elif args.args:
        code = pathlib.Path(args.args[0]).read_text()
    else:
        args.interactive = True

    if code is not None:
        engine.add_text(code)
        engine.run()

    if args.interactive:
        while True:
            stack_depth = len(engine.estate.ostack)
            try:
                line = input_fn(f"|-{stack_depth}> ")
            except EOFError:
                print()
                break
            try:
                engine.add_text(line)
                engine.run()
            except Tilted as err:
                print(f"!!! {err}")

    return 0

if __name__ == "__main__":          # pragma: no cover
    sys.exit(main(sys.argv[1:]))
