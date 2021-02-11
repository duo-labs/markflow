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

from ._lines import is_atx_heading_line


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
        otherwise it is an empty list. The second value is the remaining text. (If lines
        does not start with an ATX heading, it is the same as lines.)
    """
    if is_atx_heading_line(lines[0]):
        return [lines[0]], lines[1:]
    else:
        return [], lines
