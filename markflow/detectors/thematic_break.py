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

from .._utils import get_indent

SEPARATOR_SYMBOLS = ["*", "_", "-"]


def thematic_break_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    if get_indent(line) >= 4:
        return False

    spaceless_line = "".join(line.split())
    if len(spaceless_line) < 3:
        # Thematic breaks must be at least three characters long
        return False
    else:
        for symbol in SEPARATOR_SYMBOLS:
            if all(char == symbol for char in spaceless_line.strip()):
                return True
        return False


def thematic_break_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return True


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
        found, otherwise it is `None`. The second value is the remaining text. (If lines
        does not start with a thematic break, it is the same as lines.)
    """
    thematic_break = []
    remaining_lines = lines

    spaceless_line = "".join(lines[0].split())

    if get_indent(lines[0]) > 4:
        pass
    elif len(spaceless_line) < 3:
        # Thematic breaks must be at least three characters long
        pass
    else:
        for symbol in SEPARATOR_SYMBOLS:
            if all(char == symbol for char in spaceless_line.strip()):
                thematic_break.append(lines[0])
                remaining_lines = lines[1:]

    return thematic_break, remaining_lines
