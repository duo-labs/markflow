import re

from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownFootnote"]

POST_COLON_SPACE_REGEX = re.compile(r":\s+")


class MarkdownFootnote(MarkdownSection):
    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        reformatted_lines = []
        for line in self.lines:
            reformatted_lines.append(
                POST_COLON_SPACE_REGEX.sub(": ", line.strip(), count=1)
            )
        return "\n".join(reformatted_lines)
