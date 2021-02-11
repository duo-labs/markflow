"""
MarkFlow Thematic Break Detection Library

A thematic break is a lines that is a sequence of at least three dashes (-), underscores
(_), or asterisks (*), with optional whitespace (though no more that three leading
spaces), and is not the underlining of a setext heading in the case of dashes.

Examples:
    ```
    ___
    ```

    ```
    ****************
    ```
"""

from typing import List, Tuple

from ._lines import is_thematic_break_line

SEPARATOR_SYMBOLS = ["*", "_", "-"]


def split_thematic_break(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split leading thematic break from lines if one exists

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the indented code block lines if they were
        found, otherwise it is an empty list. The second value is the remaining text.
        (If lines does not start with a thematic break, it is the same as lines.)
    """
    if is_thematic_break_line(lines[0]):
        return [lines[0]], lines[1:]
    else:
        return [], lines
