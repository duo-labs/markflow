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

from .._utils import truncate_str
from .._utils.textwrap import wrap
from ..typing import Number
from .base import MarkdownSection

__all__ = ["MarkdownSetextHeading"]

REPR_CONTENT_LEN = 20


class MarkdownSetextHeading(MarkdownSection):
    @property
    def char(self) -> str:
        if len(self.lines) < 2:
            raise RuntimeError(
                f"Attempted access of uninitialized {self.__class__.__name__}."
            )
        return self.lines[-1].strip()[0]

    @property
    def content(self) -> str:
        if len(self.lines) < 2:
            raise RuntimeError(
                f"Attempted access of uninitialized {self.__class__.__name__}."
            )
        return " ".join(line.strip() for line in self.lines[:-1])

    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        heading_str = wrap(self.content, width)
        heading_len = max(len(line) for line in heading_str.splitlines())
        return heading_str + "\n" + self.char * heading_len

    def __repr__(self) -> str:
        return (
            f"<"
            f"{self.__class__.__name__}: "
            f"char={repr(self.char)}; "
            f"content={repr(truncate_str(self.content, REPR_CONTENT_LEN))}"
            f">"
        )
