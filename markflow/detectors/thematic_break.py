"""
4.1 Thematic breaks

A line consisting of 0-3 spaces of indentation, followed by a sequence of three or more
matching -, _, or * characters, each followed optionally by any number of spaces or
tabs, forms a thematic break.

It is required that all of the non-whitespace characters be the same.

TODO: Revisit when working on lists.

When both a thematic break and a list item are possible interpretations of a line, the
thematic break takes precedence.

If you want a thematic break in a list item, use a different bullet.

https://spec.commonmark.org/0.29/#thematic-breaks
"""

from typing import List

from .code_block import indented_code_block_started

SEPARATOR_SYMBOLS = ["*", "_", "-"]


def thematic_break_started(line: str, index: int, lines: List[str]) -> bool:
    spaceless_line = "".join(line.split())
    if indented_code_block_started(line, index, lines):
        # A line consisting of more than four spaces of indentation
        # TODO: Should we move that to an explicit call instead of depending on the
        #  indented code block code. Probably.
        return False
    elif len(spaceless_line) < 3:
        # Thematic breaks must be at least three characters long
        return False
    else:
        for symbol in SEPARATOR_SYMBOLS:
            if all(char == symbol for char in spaceless_line.strip()):
                return True
        return False


def thematic_break_ended(line: str, index: int, lines: List[str]) -> bool:
    return True
