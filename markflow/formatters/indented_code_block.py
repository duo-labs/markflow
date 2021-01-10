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
import logging

from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownIndentedCodeBlock"]

logger = logging.getLogger(__name__)

REPR_CONTENT_LEN = 20


class MarkdownIndentedCodeBlock(MarkdownSection):
    @property
    def first_line(self) -> str:
        return self.lines[0].strip()

    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        return "\n".join([line.rstrip() for line in self.lines])

    def __repr__(self) -> str:
        first_line = self.first_line
        if len(first_line) > REPR_CONTENT_LEN:
            first_line = first_line[: (REPR_CONTENT_LEN - 3)] + "..."
        return f"<{self.__class__.__name__}: first_line={repr(first_line)}>"
