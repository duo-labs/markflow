"""
4.2 ATX headings

An ATX heading consists of a string of characters, parsed as inline content, between an
opening sequence of 1–6 unescaped # characters and an optional closing sequence of any
number of unescaped # characters. The opening sequence of # characters must be followed
by a space or by the end of line. The optional closing sequence of #s must be preceded
by a space and may be followed by spaces only. The opening # character may be indented
0-3 spaces. The raw contents of the heading are stripped of leading and trailing spaces
before being parsed as inline content. The heading level is equal to the number of #
characters in the opening sequence.

At least one space is required between the # characters and the heading’s contents,
unless the heading is empty. Note that many implementations currently do not require the
space. However, the space was required by the original ATX implementation.

https://spec.commonmark.org/0.29/#atx-headings
"""

from typing import List

from .indented_code_block import indented_code_block_started


def atx_heading_started(line: str, index: int, lines: List[str]) -> bool:
    # The standard says we must require a space, but it also notes that not everyone
    # follows this. Let's be lax and fix it for them in the formatter.
    if line.lstrip().startswith("#") and not indented_code_block_started(
        line, index, lines
    ):
        return True
    else:
        return False


def atx_heading_ended(line: str, index: int, lines: List[str]) -> bool:
    return True
