"""Test cli.py for Stilted."""

import textwrap
from typing import Callable

import pytest

from cli import main


def fake_input(lines: str) -> Callable[[str], str]:
    """Create a fake `input` function that return lines from `lines`."""
    ilines = iter(lines.split("\n"))

    def _fake(prompt):
        print(prompt, end="")
        try:
            line = next(ilines)
            print(line)
            return line + "\n"
        except StopIteration:
            raise EOFError()

    return _fake


def test_command_line_code(capsys):
    main(["123 456 add =="])
    assert capsys.readouterr().out == "579\n"


@pytest.mark.parametrize(
    "lines, output",
    [
        (
            "123 456\nadd\n==",
            """\
                |-0> 123 456
                |-2> add
                |-1> ==
                579
                |-0>
            """,
        ),
        (
            "]",
            """\
                |-0> ]
                !!! unmatchedmark
                |-0>
            """,
        ),
    ],
)
def test_prompting(capsys, lines, output):
    main([], input_fn=fake_input(lines))
    assert capsys.readouterr().out.rstrip() == textwrap.dedent(output).rstrip()
