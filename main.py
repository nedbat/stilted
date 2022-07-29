"""Main program for CLI usage of Stilted."""

import sys

from estate import ExecState
from evaluate import evaluate, add_text, execute

def main(argv):
    if argv:
        evaluate(' '.join(argv))
    else:
        estate = ExecState.new()
        while True:
            stack_depth = len(estate.ostack)
            try:
                line = input(f"|-{stack_depth}> ")
            except EOFError:
                print()
                break
            add_text(estate, line)
            execute(estate)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
