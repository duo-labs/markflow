from ..typing import Number

from .base import MarkdownSection
from .textwrap import wrap

__all__ = ["MarkdownParagraph"]


class MarkdownParagraph(MarkdownSection):
    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        return wrap(" ".join([line.strip() for line in self.lines]), width)
