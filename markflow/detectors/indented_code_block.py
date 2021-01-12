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
