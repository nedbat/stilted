"""Main program for CLI usage of Stilted."""

import sys

from error import Tilted
from evaluate import evaluate, Engine


def main(argv):
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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
