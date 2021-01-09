"""
4.3 Setext headings

A setext heading consists of one or more lines of text, each containing at least one
non-whitespace character, with no more than 3 spaces indentation, followed by a setext
heading underline. The lines of text must be such that, were they not followed by the
setext heading underline, they would be interpreted as a paragraph: they cannot be
interpretable as a code fence, ATX heading, block quote, thematic break, list item, or
HTML block.

A setext heading underline is a sequence of = characters or a sequence of - characters,
with no more than 3 spaces indentation and any number of trailing spaces. If a line
containing a single - can be interpreted as an empty list items, it should be
interpreted this way and not as a setext heading underline.

The heading is a level 1 heading if = characters are used in the setext heading
underline, and a level 2 heading if - characters are used. The contents of the heading
are the result of parsing the preceding lines of text as CommonMark inline content.

In general, a setext heading need not be preceded or followed by a blank line. However,
it cannot interrupt a paragraph, so when a setext heading comes after a paragraph, a
blank line is needed between them.

https://spec.commonmark.org/0.29/#setext-headings
"""

from typing import List

from .code_block import indented_code_block_started
from .list import list_started
from .paragraph import paragraph_started, paragraph_ended


def setext_heading_started(line: str, index: int, lines: List[str]) -> bool:
    if list_started(line, index, lines):
        # Lists can't be headings
        return False
    elif indented_code_block_started(line, index, lines):
        # TODO: This should likely detect more than three spaces of indentation.
        return False

    # Avoid looking beyond the end of the file. This is clearly not a setext heading at
    # that point.
    if len(lines) <= index + 1:
        return False

    # We're basically checking if the lines up to the underlining could be a paragraph.
    # We could also move to checking not this: code fence, ATX heading, block quote,
    # thematic break, list item, or HTML block, though that may be more useful in the
    # paragraph detector.
    potential_lines = []
    for j, potential_line in enumerate(lines[index:]):
        if setext_heading_ended(potential_line, index + j, lines):
            break
        else:
            potential_lines.append(potential_line)

    # TODO: Change when detectors are classes or something more reasonable
    if not paragraph_started(potential_lines[0], 0, potential_lines):
        return False
    for potential_i, potential_line in enumerate(potential_lines[:-1]):
        if potential_i == 0:
            continue
        if paragraph_ended(potential_line, potential_i, potential_lines):
            return False

    # Assuming no matter what the last line was, it could end a paragraph.
    return True


def setext_heading_ended(line: str, index: int, lines: List[str]) -> bool:
    return line.strip() and (
        all([c == "=" for c in line.strip()]) or all([c == "-" for c in line.strip()])
    )
