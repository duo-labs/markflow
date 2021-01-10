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

from typing import List

INDENT = " " * 4


def indented_code_block_started(line: str, index: int, lines: List[str]) -> bool:
    return bool(line.strip()) and line.startswith(INDENT)


def indented_code_block_ended(line: str, index: int, lines: List[str]) -> bool:
    if not line.strip():
        # If we find a blank line, we need to check and see if the next non-blank line
        # is not indented
        for line in lines[index:]:
            # We've found a blank line
            if not line.strip():
                continue
            if line.startswith(INDENT):
                return False
            else:
                return True
        else:
            return False
    elif line.startswith(INDENT):
        return False
    else:
        return True
