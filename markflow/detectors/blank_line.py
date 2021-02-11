"""
MarkFlow Blank Line Detection Library

Blank lines are simply those lines that only have whitespace in them and are not in the
middle of another section line and indented code block.

Example:
    ```

    ```
"""

from typing import List, Tuple

from ._lines import is_blank_line_line


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
        single-element list), otherwise it is an empty list. The second value is the
        remaining text. (If lines does not start with a blank line, it is the same as
        lines.)
    """
    if is_blank_line_line(lines[0]):
        return [lines[0]], lines[1:]
    else:
        return [], lines
