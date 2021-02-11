"""
4.5 Fenced code blocks

A code fence is a sequence of at least three consecutive backtick characters (`) or
tildes (~). (Tildes and backticks cannot be mixed.) A fenced code block begins with a
code fence, indented no more than three spaces.

The line with the opening code fence may optionally contain some text following the
code fence; this is trimmed of leading and trailing whitespace and called the info
string. If the info string comes after a backtick fence, it may not contain any backtick
characters. (The reason for this restriction is that otherwise some inline code would
be incorrectly interpreted as the beginning of a fenced code block.)

The content of the code block consists of all subsequent lines, until a closing code
fence of the same type as the code block began with (backticks or tildes), and with at
least as many backticks or tildes as the opening code fence. If the leading code fence
is indented N spaces, then up to N spaces of indentation are removed from each line of
the content (if present). (If a content line is not indented, it is preserved unchanged.
If it is indented less than N spaces, all of the indentation is removed.)

The closing code fence may be indented up to three spaces, and may be followed only by
spaces, which are ignored. If the end of the containing block (or document) is reached
and no closing code fence has been found, the code block contains all of the lines after
the opening code fence until the end of the containing block (or document). (An
alternative spec would require backtracking in the event that a closing code fence is
not found. But this makes parsing much less efficient, and there seems to be no real
down side to the behavior described here.)

A fenced code block may interrupt a paragraph, and does not require a blank line either
before or after.

https://spec.commonmark.org/0.29/#fenced-code-blocks
"""

from typing import Optional

from .._utils import truncate_str
from ..typing import Number
from .base import MarkdownSection

__all__ = ["MarkdownFencedCodeBlock"]

REPR_CONTENT_LEN = 20


class MarkdownFencedCodeBlock(MarkdownSection):
    @property
    def fence_char(self) -> str:
        return self.lines[0].strip()[0]

    @property
    def fence_count(self) -> int:
        return len(self.lines[0].strip()) - len(
            self.lines[0].strip().lstrip(self.fence_char)
        )

    @property
    def first_line(self) -> Optional[str]:
        if len(self.lines) == 2:
            return None
        else:
            return self.lines[1].strip()

    @property
    def language(self) -> str:
        return self.lines[0].strip().lstrip(self.fence_char).strip()

    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        fence = self.fence_char * self.fence_count
        new_lines = [fence + self.language] + self.lines[1:-1] + [fence]
        return "\n".join([line.rstrip() for line in new_lines])

    def __repr__(self) -> str:
        first_line = self.first_line
        if first_line is not None:
            first_line = truncate_str(first_line, REPR_CONTENT_LEN)
        return (
            f"<"
            f"{self.__class__.__name__}: "
            f"fence_char={repr(self.fence_char)}; "
            f"fence_count={repr(self.fence_count)}; "
            f"language={repr(self.language)}; "
            f"first_line={repr(first_line)}"
            f">"
        )
