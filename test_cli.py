"""Test cli.py for Stilted."""

import textwrap
from typing import Callable, Iterable

import pytest

from cli import main


def fake_input(lines: Iterable[str]) -> Callable[[str], str]:
    """Create a fake `input` function that return lines from `lines`."""
    ilines = iter(lines)

    def _fake(prompt):
        print(prompt, end="")
        try:
            line = next(ilines)
            print(line)
            return line + "\n"
        except StopIteration:
            raise EOFError()

    return _fake


@pytest.mark.parametrize(
    "argv, lines, output",
    [
        (
            [],
            ["123 456", "add", "=="],
            """\
                |-0> 123 456
                |-2> add
                |-1> ==
                579
                |-0>
            """,
        ),
        (
            [],
            ["]"],
            """\
                |-0> ]
                !!! unmatchedmark
                |-0>
            """,
        ),
        (
            ["-c", "123 456 add dup =="],
            [],
            """\
                579
            """,
        ),
        (
            ["-i", "-c", "123 456 add dup =="],
            ["dup 2 mul pstack"],
            """\
                579
                |-1> dup 2 mul pstack
                1158
                579
                |-2>
            """,
        ),
    ],
)
def test_prompting(capsys, argv, lines, output):
    main(argv, input_fn=fake_input(lines))
    assert capsys.readouterr().out.rstrip() == textwrap.dedent(output).rstrip()


def test_file_input(capsys, tmp_path):
    foo_ps = tmp_path / "foo.ps"
    foo_ps.write_text("123 456\n add\n ==\n")
    main([str(foo_ps)])
    assert capsys.readouterr().out == "579\n"
