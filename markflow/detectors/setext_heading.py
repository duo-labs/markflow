"""
MarkFlow Setext Heading Detection Library

Setext headings are basically any paragraph that is followed by a line composed of all
all equals signs (=) or dashes (-). The former indicates a heading of level 1 while the
latter indicates a heading of level 2.

Examples:
    ```
    Heading 1
    =========
    ```

    ```
    Heading 2
    -
    ```
"""

from typing import List, Tuple

from ._lines import is_setext_underline
from .paragraph import split_paragraph_ignoring_setext


def split_setext_heading(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split setext heading from beginning of lines if one exists

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the setext heading lines if they were found,
        otherwise it is an empty list. The second value is the remaining text. (If lines
        does not start with a thematic break, it is the same as lines.)
    """
    paragraph, remaining_lines = split_paragraph_ignoring_setext(lines, line_offset)
    if paragraph and remaining_lines and is_setext_underline(remaining_lines[0]):
        return paragraph + [remaining_lines[0]], remaining_lines[1:]
    return [], lines
