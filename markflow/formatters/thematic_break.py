import math

from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownThematicBreak"]


class MarkdownThematicBreak(MarkdownSection):
    def append(self, line: str) -> None:
        if self.lines:
            raise RuntimeError("Thematic breaks cannot span multiple lines")
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        char = self.lines[0].strip()[0]
        if isinstance(width, float):
            if width == math.inf:
                return char * 3
            else:
                raise RuntimeError(
                    f"Invalid width {repr(width)} passed. How did you manage this?"
                )
        else:
            return char * width
