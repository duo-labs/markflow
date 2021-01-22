"""
MarkFlow Blank Line Detection Library

Blank lines are simply those lines that only have whitespace in them and are not in the
middle of another section line and indented code block.

Example:
    ```

    ```
"""

"""
4.9 Blank lines

Blank lines between block-level elements are ignored, except for the role they play in
determining whether a list is tight or loose.

Blank lines at the beginning and end of the document are also ignored.

https://spec.commonmark.org/0.29/#blank-lines
"""

from typing import List, Tuple


def blank_line_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return not line.strip()


def blank_line_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return True


def split_blank_line(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split leading blank line from lines if one exists

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the blank line if it was found (as a
        single-element list), otherwise it is `None`. The second value is the remaining
        text. (If lines does not start with a blank line, it is the same as lines.)
    """
    blank_line = []
    remaining_lines = lines

    if not lines[0].strip():
        blank_line = [lines[0]]
        remaining_lines = lines[1:]

    return blank_line, remaining_lines
