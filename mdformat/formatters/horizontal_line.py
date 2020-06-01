import math

from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownHorizontalLine"]


class MarkdownHorizontalLine(MarkdownSection):
    def append(self, line: str) -> None:
        if self.lines:
            raise RuntimeError("Horizontal lines cannot span multiple lines")
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        if isinstance(width, float):
            if width == math.inf:
                return "-" * 3
            else:
                raise RuntimeError(
                    f"Invalid width {repr(width)} passed. How did you manage this?"
                )
        else:
            return "-" * width
