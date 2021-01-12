"""
4.9 Blank lines

Blank lines between block-level elements are ignored, except for the role they play in
determining whether a list is tight or loose.

Blank lines at the beginning and end of the document are also ignored.

https://spec.commonmark.org/0.29/#blank-lines
"""

from typing import List, Tuple


def blank_line_started(line: str, index: int, lines: List[str]) -> bool:
    return not line.strip()


def blank_line_ended(line: str, index: int, lines: List[str]) -> bool:
    return True


def split_blank_line(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    blank_line = []
    remaining_lines = lines

    if not lines[0].strip():
        blank_line = [lines[0]]
        remaining_lines = lines[1:]

    return blank_line, remaining_lines
