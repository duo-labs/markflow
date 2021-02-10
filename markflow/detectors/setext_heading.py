"""
Markflow Setext Heading Detection Library

Setexet headings are basically any paragraph that is followed by a line composed of all
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

from .list import list_started
from .paragraph import paragraph_started, paragraph_ended
from .._utils import get_indent


def _is_underline(str_: str) -> bool:
    return bool(str_.strip()) and (
        all([c == "=" for c in str_.strip()]) or all([c == "-" for c in str_.strip()])
    )


def setext_heading_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    if list_started(line, index, lines):
        # Lists can't be headings
        return False
    elif get_indent(line) >= 4:
        return False

    # Avoid looking beyond the end of the file. This is clearly not a setext heading at
    # that point.
    if len(lines) <= index + 1:
        return False

    # Well an underline clearly isn't a title
    if _is_underline(line):
        return False

    # We're basically checking if the lines up to the underlining could be a paragraph.
    # We could also move to checking not this: code fence, ATX heading, block quote,
    # thematic break, list item, or HTML block, though that may be more useful in the
    # paragraph detector.
    potential_lines = []
    for potential_line in lines[index:]:
        if _is_underline(potential_line):
            break
        potential_lines.append(potential_line)
    else:
        return False

    # TODO: Change when detectors are classes or something more reasonable
    # TODO: It is also likely everything before potential_lines is unnecessary.
    if not paragraph_started(potential_lines[0], 0, potential_lines):
        return False
    for potential_i, potential_line in enumerate(potential_lines):
        if potential_i == 0:
            continue
        if paragraph_ended(potential_line, potential_i, potential_lines):
            return False

    return True


def setext_heading_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return _is_underline(lines[index - 1])


def split_setext_heading(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    # ToDo: Instead of using this pattern, leverage the unified `_paragraph_split` which
    #  will provide a way to split out a paragraph, not caring if it is a setext or not.
    #  `paragraph_split` will handle that for paragraphs.
    setext_heading = []
    remaining_lines = lines

    index = 0
    if setext_heading_started(lines[index], index, lines):
        setext_heading.append(lines[index])
        for index, line in enumerate(lines[1:], start=index + 1):
            if setext_heading_ended(line, index, lines):
                break
            setext_heading.append(line)
        else:
            index += 1
    remaining_lines = lines[index:]

    return setext_heading, remaining_lines
