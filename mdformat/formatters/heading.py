from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownHeading"]


class MarkdownHeading(MarkdownSection):
    def append(self, line: str) -> None:
        if self.lines:
            if self.lines[0].startswith("#"):
                raise RuntimeError(
                    "Attempted to add a line to a header that uses #. Headers are "
                    "only only line."
                )
            elif not (
                any(c == "-" for c in line.strip())
                or any(c == "=" for c in line.strip())
            ):
                # TODO: What if the user's file causes this
                raise RuntimeError("Improper underlining passed to header.")
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        if len(self.lines) > 1:
            line_length = len(self.lines[0].strip())
            return self.lines[0].strip() + "\n" + self.lines[1].strip()[0] * line_length
        else:
            return self.lines[0].strip()
