import re

from typing import List
from ..typing import Number

from .base import MarkdownSection
from .textwrap import wrap

__all__ = ["MarkdownBlockQuote"]

NON_ESCAPED_QUOTE_MARKER = re.compile(r"(?<= )>")


class MarkdownBlockQuote(MarkdownSection):
    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        indent = len(self.lines[0].lstrip(" ")) - len(self.lines[0])
        depths: List[int] = []
        real_lines: List[str] = []

        # A new-line at any depth is required to de-indent a block-quote
        previous_line_was_blank = False
        for line in self.lines:
            current_depth = len(line.replace(" ", "")) - len(
                line.replace(" ", "").lstrip(">")
            )
            cleaned_up_line = line.strip().lstrip("> ")
            # B;ank lines always get what they want
            if not cleaned_up_line:
                real_lines.append("")
                depths.append(current_depth)
                previous_line_was_blank = True
            else:
                # We change depths if:
                # 1. We don't have a depth
                # 2. We are at a deeper depth
                # 3. The previous line was blank.
                if not depths or depths[-1] < current_depth or previous_line_was_blank:
                    real_lines.append(cleaned_up_line)
                    depths.append(current_depth)
                else:
                    real_lines[-1] += " " + cleaned_up_line
                previous_line_was_blank = False

        new_lines = []
        for depth, line in zip(depths, real_lines):
            line_prefix = " " * indent + ">" * depth + " "
            line_width = width - len(line_prefix)
            line = NON_ESCAPED_QUOTE_MARKER.sub("\\>", line)

            if line:
                for sub_line in wrap(line, line_width).splitlines():
                    new_lines.append(line_prefix + sub_line)
            else:
                new_lines.append(line_prefix.rstrip())
        return "\n".join(new_lines)
