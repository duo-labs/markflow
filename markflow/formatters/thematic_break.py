"""
4.1 Thematic breaks

A line consisting of 0-3 spaces of indentation, followed by a sequence of three or more
matching -, _, or * characters, each followed optionally by any number of spaces or
tabs, forms a thematic break.

It is required that all of the non-whitespace characters be the same.

When both a thematic break and a list item are possible interpretations of a line, the
thematic break takes precedence.

If you want a thematic break in a list item, use a different bullet.

https://spec.commonmark.org/0.29/#thematic-breaks
"""

import math

from ..typing import Number
from .base import MarkdownSection

__all__ = ["MarkdownThematicBreak"]


class MarkdownThematicBreak(MarkdownSection):
    @property
    def char(self) -> str:
        # Assuming we were passed valid data
        return self.lines[0].strip()[0]

    def append(self, line: str) -> None:
        if self.lines:
            raise RuntimeError("Thematic breaks cannot span multiple lines")
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        if isinstance(width, float):
            if width == math.inf:
                return self.char * 3
            else:
                raise RuntimeError(
                    f"Invalid width {repr(width)} passed. How did you manage this?"
                )
        else:
            return self.char * width

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: char={repr(self.char)}>"
