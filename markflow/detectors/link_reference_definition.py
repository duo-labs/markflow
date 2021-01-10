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

from typing import List


FOOTNOTE_REGEX = re.compile(r"\s*\[[^\]]+\]\s*:")


def link_reference_definition_started(line: str, index: int, lines: List[str]) -> bool:
    return bool(FOOTNOTE_REGEX.search(line))


def link_reference_definition_ended(line: str, index: int, lines: List[str]) -> bool:
    return not link_reference_definition_started(line, index, lines)
