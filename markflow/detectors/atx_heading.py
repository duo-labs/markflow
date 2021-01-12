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

from typing import List, Tuple

from .._utils import get_indent


def split_atx_heading(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    atx_headings = []
    remaining_lines = lines

    if get_indent(lines[0]) >= 4:
        pass
    elif lines[0].lstrip().startswith("#"):
        # The standard says we must require a space, but it also notes that not everyone
        # follows this. Let's be lax and fix it for them in the formatter.
        atx_headings = [lines[0]]
        remaining_lines = lines[1:]
    else:
        pass

    return atx_headings, remaining_lines


def atx_heading_started(line: str, index: int, lines: List[str]) -> bool:
    if get_indent(line) >= 4:
        return False

    # The standard says we must require a space, but it also notes that not everyone
    # follows this. Let's be lax and fix it for them in the formatter.
    if line.lstrip().startswith("#"):
        return True
    else:
        return False


def atx_heading_ended(line: str, index: int, lines: List[str]) -> bool:
    return True
