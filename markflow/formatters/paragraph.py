from ..typing import Number

from .base import MarkdownSection
from .textwrap import wrap

__all__ = ["MarkdownParagraph"]


class MarkdownParagraph(MarkdownSection):
    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        text = wrap(" ".join([line.strip() for line in self.lines]), width)
        if self.lines[-1].endswith("  "):
            text += "  "
        return text
