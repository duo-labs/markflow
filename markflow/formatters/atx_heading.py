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
import logging

from .._utils import truncate_str
from ..typing import Number
from .base import MarkdownSection

__all__ = ["MarkdownATXHeading"]

logger = logging.getLogger(__name__)

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
    def depth(self) -> int:
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
        # TODO: This prints out twice. We probably need a first pass step that calls out
        #  errors we will be fixing to suppress extra statements from reprocessing the
        #  document.
        if not self.lines[0].strip().lstrip("#").startswith(" "):
            logger.warning(
                "Line %d is an ATX Header without a space after #'s. This has been "
                "corrected.",
                self.line_index + 1,
            )
        return "#" * self.depth + " " + self.content

    def __repr__(self) -> str:
        return (
            f"<"
            f"{self.__class__.__name__}: "
            f"depth={repr(self.depth)}; "
            f"content={repr(truncate_str(self.content, REPR_CONTENT_LEN))}"
            f">"
        )
