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

    def __repr__(self):
        return f"<{self.__class__.__name__}: char={repr(self.char)}>"
