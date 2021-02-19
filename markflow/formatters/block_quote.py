import logging
import re
from typing import List

from .._utils import get_indent, redirect_info_logs_to_debug, truncate_str
from ..detectors._lines import is_explicit_block_quote_line
from ..typing import Number
from .base import MarkdownSection

__all__ = ["MarkdownBlockQuote"]

REPR_CONTENT_LEN = 20
NON_ESCAPED_QUOTE_MARKER = re.compile(r"(?<= )>")
LEADING_QUOTE_MARKER = re.compile(r"^ {0,3}>")

logger = logging.getLogger(__name__)


def _reformat_markdown(lines: List[str], width: Number) -> str:
    # Prevents issues from circular imports. Since this module would already be loaded
    # whenever we call this function, we know it's cached.
    from ..reformat_markdown import _reformat_markdown_text

    with redirect_info_logs_to_debug():
        text = _reformat_markdown_text("\n".join(lines) + "\n", width)

    return text


class MarkdownBlockQuote(MarkdownSection):
    @property
    def first_line(self) -> str:
        return self.lines[0]

    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        indent = len(self.lines[0].lstrip()) - len(self.lines[0])

        depth = 0
        fully_quoted_lines = []
        for line in self.lines:
            if is_explicit_block_quote_line(line):
                spaceless_string = "".join(line.split())
                depth = len(spaceless_string) - len(spaceless_string.lstrip(">"))
                fully_quoted_lines.append(line)
            else:
                fully_quoted_lines.append((">" * depth) + line)

        stripped_lines: List[str] = []
        for line in fully_quoted_lines:
            stripped_lines.append(LEADING_QUOTE_MARKER.sub("", line))

        for line in stripped_lines:
            if not line.strip():
                continue
            if get_indent(line) == 1:
                has_space = True
                break
            elif get_indent(line) == 0:
                has_space = False
                break
        else:
            has_space = False

        if has_space:
            restripped_lines: List[str] = []
            for line in stripped_lines:
                restripped_lines += [line[1:] if line and line[0] == " " else line]
            stripped_lines = restripped_lines

        sub_width = width - indent - 1
        prefix = " " * indent + ">"
        if has_space:
            sub_width -= 1
            prefix += " "

        # ToDo (jmholla): Issues with leading > in paragraphs will be handled by a later
        #  change.
        text = _reformat_markdown(stripped_lines, width=sub_width)
        text = "\n".join((prefix + line).strip() for line in text.splitlines())

        return text

    def __repr__(self) -> str:
        first_line = self.first_line
        if first_line is not None:
            first_line = truncate_str(first_line, REPR_CONTENT_LEN)
        return f"{self.__class__.__name__}: first_line={repr(first_line)}>"
