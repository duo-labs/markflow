"""
4.9 Blank lines

Blank lines between block-level elements are ignored, except for the role they play in
determining whether a list is tight or loose.

Blank lines at the beginning and end of the document are also ignored.

https://spec.commonmark.org/0.29/#blank-lines
"""

from typing import List


def blank_line_started(line: str, index: int, lines: List[str]) -> bool:
    return not line.strip()


def blank_line_ended(line: str, index: int, lines: List[str]) -> bool:
    return True
