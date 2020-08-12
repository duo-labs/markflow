from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownSeparator"]


class MarkdownSeparator(MarkdownSection):
    def append(self, line: str) -> None:
        if line.strip():
            raise RuntimeError(
                "Created a separator which contained non-whitespace characters"
            )
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        # We remove one new line as we will be adding it when we join sections
        return "\n" * (len(self.lines) - 1)
