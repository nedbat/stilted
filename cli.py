"""Main program for CLI usage of Stilted."""

import argparse
import pathlib
import sys
from typing import Callable

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
    parser.add_argument(
        "-o", dest="outfile", default="page.svg",
        help="Output file name. %%d will be the page number.",
    )
    parser.add_argument("args", nargs="*")

    args = parser.parse_args(argv)

    code = None
    if args.code is not None:
        code = args.code
        in_argv = ["-c"] + args.args
    elif args.args:
        code = pathlib.Path(args.args[0]).read_text()
        in_argv = args.args
    else:
        args.interactive = True
        in_argv = [""]

    engine = Engine(outfile=args.outfile)

    engine.exec_text("/argv [")
    for arg in in_argv:
        engine.push_string(arg)
    engine.exec_text("] def")

    if code is not None:
        engine.push_string(code)
        engine.exec_text("cvx stopped { handleerror } if")

    if args.interactive:
        while True:
            stack_depth = len(engine.ostack)
            try:
                line = input_fn(f"|-{stack_depth}> ")
            except EOFError:
                print()
                break
            engine.push_string(line)
            engine.exec_text("cvx stopped { handleerror } if")

    return 0

if __name__ == "__main__":          # pragma: no cover
    sys.exit(main(sys.argv[1:]))
