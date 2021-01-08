"""
4.2 ATX headings

An ATX heading consists of a string of characters, parsed as inline content, between an
opening sequence of 1–6 unescaped # characters and an optional closing sequence of any
number of unescaped # characters. The opening sequence of # characters must be followed
by a space or by the end of line. The optional closing sequence of #s must be preceded
by a space and may be followed by spaces only. The opening # character may be indented
0-3 spaces. The raw contents of the heading are stripped of leading and trailing spaces
before being parsed as inline content. The heading level is equal to the number of #
characters in the opening sequence.

At least one space is required between the # characters and the heading’s contents,
unless the heading is empty. Note that many implementations currently do not require the
space. However, the space was required by the original ATX implementation.

https://spec.commonmark.org/0.29/#atx-headings
"""

from typing import Optional

from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownATXHeading"]

REPR_CONTENT_LEN = 20


class MarkdownATXHeading(MarkdownSection):
    @property
    def content(self) -> str:
        if not self.lines:
            raise RuntimeError(
                f"Attempted access of uninitialized {self.__class__.__name__}."
            )
        return self.lines[0].strip().lstrip("#").strip()

    @property
    def depth(self) -> Optional[int]:
        if not self.lines:
            raise RuntimeError(
                f"Attempted access of uninitialized {self.__class__.__name__}."
            )
        return len(self.lines[0].strip()) - len(self.lines[0].strip().lstrip("#"))

    def append(self, line: str) -> None:
        if self.lines:
            raise RuntimeError(
                "Attempted to add another line to an ATX Header. They can only be one "
                "line."
            )
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        return "#" * self.depth + " " + self.content

    def __repr__(self):
        printable_content = self.content
        if len(printable_content) > REPR_CONTENT_LEN:
            printable_content = printable_content[:(REPR_CONTENT_LEN - 3)] + "..."
        return (
            f"<"
            f"{self.__class__.__name__}: "
            f"depth={self.depth}; "
            f"content={repr(printable_content)}"
            f">"
        )
