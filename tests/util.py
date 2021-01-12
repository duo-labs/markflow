import re

from typing import Type

import commonmark

from markflow.formatters import MarkdownSection

IGNORED_HTML_CHARACTERS = re.compile(r"[\n\s]")
# We need to remove starts to ignore our numbering corrections.
LIST_NUMBERING_START = re.compile(r" start=\"[0-9]+\"")


def create_section(class_: Type[MarkdownSection], text: str) -> MarkdownSection:
    obj = class_(0, text.splitlines())
    return obj


def render(text: str) -> str:
    rendered = commonmark.commonmark(text)
    rendered = LIST_NUMBERING_START.sub("", rendered)
    rendered = IGNORED_HTML_CHARACTERS.sub("", rendered)
    return rendered
