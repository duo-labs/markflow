"""
4.9 Blank lines

Blank lines between block-level elements are ignored, except for the role they play in
determining whether a list is tight or loose.

Blank lines at the beginning and end of the document are also ignored.

https://spec.commonmark.org/0.29/#blank-lines
"""

from ..typing import Number
from .base import MarkdownSection

__all__ = ["MarkdownBlankLine"]


class MarkdownBlankLine(MarkdownSection):
    def append(self, line: str) -> None:
        if line.strip():
            raise RuntimeError(
                f"A line with non-whitespace characters has been added to a "
                f"`{self.__class__.__name__}`. Please open a bug report or email "
                f"jholland@duosecurity.com."
            )
        if self.lines:
            raise RuntimeError(
                f"`{self.__class__.__name__}`s can only contain one line. Please open "
                f"a bug report or email jholland@duosecurity.com."
            )
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        # The new line will be added on join
        return ""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
