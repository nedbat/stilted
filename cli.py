"""Main program for CLI usage of Stilted."""

import sys
from typing import Callable

from error import Tilted
from evaluate import evaluate, Engine


def main(argv: list[str], input: Callable[[str], str]=input) -> int:
    if argv:
        evaluate(' '.join(argv))
    else:
        engine = Engine()
        while True:
            stack_depth = len(engine.estate.ostack)
            try:
                line = input(f"|-{stack_depth}> ")
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
