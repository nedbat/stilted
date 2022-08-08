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
                Error: unmatchedmark in --]--
                Operand stack (0):
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
        (
            ["-i", "-c", ""],
            ["0 1 1 10 { add } for =="],
            """\
                |-0> 0 1 1 10 { add } for ==
                55
                |-0>
            """,
        ),
        (
            ["-i", "-c", "", "abc", "def"],
            ["argv pstack"],
            """\
                |-0> argv pstack
                [(-c) (abc) (def)]
                |-1>
            """,
        ),
        (
            ["-c", "argv pstack", "hello", "123"],
            [],
            """\
                [(-c) (hello) (123)]
            """,
        ),
    ],
)
def test_prompting(capsys, argv, lines, output):
    main(argv, input_fn=fake_input(lines))
    assert capsys.readouterr().out.rstrip() == textwrap.dedent(output).rstrip()


@pytest.mark.parametrize(
    "file_text, output",
    [
        ("123 456\n add\n ==\n argv pstack", "579\n[({fname}) (abc)]\n"),
        ("123 (a) add\n", "Error: typecheck in --add--\nOperand stack (2):\n(a)\n123\n"),
    ],
)
def test_file_input(file_text, output, capsys, tmp_path):
    foo_ps = tmp_path / "foo.ps"
    foo_ps.write_text(file_text)
    fname = str(foo_ps)
    main([fname, "abc"])
    assert capsys.readouterr().out == output.format(fname=fname)
