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

A link label begins with a left bracket ([) and ends with the first right bracket (])
that is not backslash-escaped. Between these brackets there must be at least one non-
whitespace character. Unescaped square bracket characters are not allowed inside the
opening and closing square brackets of link labels. A link label can have at most 999
characters inside the square brackets.

https://spec.commonmark.org/0.29/#link-label
"""

import re

from ..typing import Number

from .base import MarkdownSection
from .util import truncate_str

__all__ = ["MarkdownLinkReferenceDefinition"]

POST_COLON_SPACE_REGEX = re.compile(r":\s+")
REPR_CONTENT_LEN = 20
LINK_REFERENCE_DEFINITION_REGEX = re.compile(
    r"\["
    r"(?P<name>[^\]]{1,999})"
    r"\]:"
    r"\s*"
    r"(?P<link>[^\s]*)"
    r"\s*"
    r"(?P<title>.*)"
)


class MarkdownLinkReferenceDefinition(MarkdownSection):
    @property
    def name(self) -> str:
        match = LINK_REFERENCE_DEFINITION_REGEX.search(" ".join(self.lines))
        if match is None:
            raise RuntimeError(
                "Invalid link reference definition created. Please open a bug report "
                "or email jholland@duoescurity.com."
            )
        return match.group("name")

    @property
    def link(self) -> str:
        match = LINK_REFERENCE_DEFINITION_REGEX.search(" ".join(self.lines))
        if match is None:
            raise RuntimeError(
                "Invalid link reference definition created. Please open a bug report "
                "or email jholland@duoescurity.com."
            )
        return match.group("link")

    @property
    def title(self) -> str:
        match = LINK_REFERENCE_DEFINITION_REGEX.search(" ".join(self.lines))
        if match is None:
            raise RuntimeError(
                "Invalid link reference definition created. Please open a bug report "
                "or email jholland@duoescurity.com."
            )
        title = match.group("title")
        return " ".join(title.split())

    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        str_ = f"[{self.name}]:"
        if self.link in self.lines[0]:
            str_ += f" {self.link}"
        else:
            str_ += f"\n{self.link}"
        str_ += self.link

        # if " " in self.title and self.title
        reformatted_lines = []
        for line in self.lines:
            reformatted_lines.append(
                POST_COLON_SPACE_REGEX.sub(": ", line.strip(), count=1)
            )
        return "\n".join(reformatted_lines)

    def __repr__(self) -> str:
        return (
            f"<"
            f"{self.__class__.__name__}: "
            f"name={truncate_str(self.name, REPR_CONTENT_LEN)} "
            f"link={truncate_str(self.link, REPR_CONTENT_LEN)} "
            f"title={truncate_str(self.title, REPR_CONTENT_LEN)}"
            f">"
        )
