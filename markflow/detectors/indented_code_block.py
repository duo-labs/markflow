"""
MarkFlow Indented Code Block Detection Library

Indented code blocks are one or more lines of text that are indented at least four
spaces that are not in the middle of a paragraph.

Example:
    ```
        print("Hello world!")
    ```
"""

"""
4.4 Indented code blocks

An indented code block is composed of one or more indented chunks separated by blank
lines. An indented chunk is a sequence of non-blank lines, each indented four or more
spaces. The contents of the code block are the literal contents of the lines, including
trailing line endings, minus four spaces of indentation. An indented code block has no
info string.

An indented code block cannot interrupt a paragraph, so there must be a blank line
between a paragraph and a following indented code block. (A blank line is not needed,
however, between a code block and a following paragraph.)

TODO: Keep in mind for paragraphs

https://spec.commonmark.org/0.29/#indented-code-blocks
"""

from typing import List, Tuple

from .._utils import get_indent


def split_indented_code_block(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split leading indented code block from lines if one exists

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the indented code block lines if they were
        found, otherwise it is `None`. The second value is the remaining text. (If lines
        does not start with an indented code block, it is the same as lines.)
    """
    indented_code_block = []
    remaining_lines = lines
    indexed_line_generator = enumerate(lines)

    # By default, everything to the end of the document is a block quote
    index, line = next(indexed_line_generator)
    close_index = index + 1
    if line.strip() and get_indent(line) >= 4:
        # Find the next line that isn't indented at least 4, excluding trailing blank
        # lines
        for index, line in indexed_line_generator:
            if not line.strip():
                continue
            elif get_indent(line) >= 4:
                close_index = index
            else:
                break

        indented_code_block = lines[:close_index]
        remaining_lines = lines[close_index:]

    return indented_code_block, remaining_lines
