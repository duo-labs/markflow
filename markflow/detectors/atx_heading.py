"""
MarkFlow ATX Heading Detection Library

ATX headings are lines that begin with ane or more octothorpes (#) and are not indented.
The number of octothorpes indicates the depth of the heading (e.g. # -> <h1></h1>,
## -> <h2></h2>) The standard requires that a space exist between the octothorpes and
the title, but our detector does not enforce that as we assume that is not actually
meant (as many other tools do) and the formatter will insert that space automatically.

Examples:
    ```
    # Heading 1
    ```

    ```
    ## Heading 2
    ```
"""

from typing import List, Tuple

from .._utils import get_indent


def split_atx_heading(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split leading ATX heading from lines if one exists

    While the standard does require that ATX headings have a space between the
    octothorpes and the heading text, we are lenient and do not require that assuming
    that to just be author error.

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the ATX heading lines if they were found,
        otherwise it is `None`. The second value is the remaining text. (If lines does
        not start with an ATX heading, it is the same as lines.)
    """
    atx_headings = []
    remaining_lines = lines

    if get_indent(lines[0]) >= 4:
        pass
    elif lines[0].lstrip().startswith("#"):
        # The standard says we must require a space, but it also notes that not everyone
        # follows this. Let's be lax and fix it for them in the formatter.
        # ToDo: warn?
        atx_headings = [lines[0]]
        remaining_lines = lines[1:]
    else:
        pass

    return atx_headings, remaining_lines


def atx_heading_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    if get_indent(line) >= 4:
        return False

    # The standard says we must require a space, but it also notes that not everyone
    # follows this. Let's be lax and fix it for them in the formatter.
    if line.lstrip().startswith("#"):
        return True
    else:
        return False


def atx_heading_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return True
