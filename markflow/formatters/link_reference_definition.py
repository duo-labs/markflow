"""
4.7 Link reference definitions

A link reference definition consists of a link label, indented up to three spaces,
followed by a colon (:), optional whitespace (including up to one line ending), a link
destination, optional whitespace (including up to one line ending), and an optional link
title, which if it is present must be separated from the link destination by whitespace.
No further non-whitespace characters may occur on the line.

A link reference definition does not correspond to a structural element of a document.
Instead, it defines a label which can be used in reference links and reference-style
images elsewhere in the document. Link reference definitions can come either before or
after the links that use them.

https://spec.commonmark.org/0.29/#link-reference-definitions
"""

import re

from ..typing import Number

from .base import MarkdownSection

__all__ = ["MarkdownLinkReferenceDefinition"]

POST_COLON_SPACE_REGEX = re.compile(r":\s+")


class MarkdownLinkReferenceDefinition(MarkdownSection):
    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        reformatted_lines = []
        for line in self.lines:
            reformatted_lines.append(
                POST_COLON_SPACE_REGEX.sub(": ", line.strip(), count=1)
            )
        return "\n".join(reformatted_lines)
