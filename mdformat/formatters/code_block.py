from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownCodeBlock"]


class MarkdownCodeBlock(MarkdownSection):
    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        return "\n".join([line.rstrip() for line in self.lines])
