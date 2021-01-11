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

import itertools
import logging
import re

from typing import List

logger = logging.getLogger(__name__)

LINK_REFERENCE_DEFINITION_FIRST_ELEMENT_REGEX = re.compile(
    r" {0,3}"  # Indent
    r"\["  # Open bracket
    r"[^\]]{1,999}"  # At least one and up to 999 characters as the name
    r"\]:"  # End bracket and colon
)

# Blech
__QUOTATION = "ERROR"
__END_INDEX = -1


def link_reference_definition_started(line: str, index: int, lines: List[str]) -> bool:
    global __END_INDEX
    global __QUOTATION

    match = LINK_REFERENCE_DEFINITION_FIRST_ELEMENT_REGEX.match(line)
    if not match:
        return False

    # We've already validated that the first word is the link definition
    rest_of_line = line[match.end() :]  # noqa: E203
    url_and_title = rest_of_line.split(maxsplit=1)
    # At the end of this, index is set to the line with the beginning of the title and
    # rest of line contains the title whether, even if it is the entire line. If there
    # is no title, we exit in here.
    # URL index will be set to the URL index only if in the event that we don't find a
    # title, it's not on the same line as the URL and label so we still have a LRD, just
    # not one with a title.
    url_index = None
    if len(url_and_title) == 1:
        # The URL is also present on the first line
        if index + 1 == len(lines):
            # We're at the end of the document
            __END_INDEX = index + 1
            return True
        if lines[index + 1].lstrip().startswith("'") or lines[
            index + 1
        ].lstrip().startswith('"'):
            # The next line starts a potential title
            rest_of_line = lines[index + 1]
            index += 1
            url_index = index
        else:
            # There's no title so the reference is complete.
            __END_INDEX = index + 1
            return True
    elif len(url_and_title) == 2:
        # The label, URL, and title are on this line, assuming the title is quoted
        if url_and_title[1].startswith("'") or url_and_title[1].startswith('"'):
            rest_of_line = url_and_title[1]
            # index = index
        else:
            return False
    else:
        # Just the label is on the first line
        if not lines[index + 1].strip() or lines[index + 1].startswith("["):
            # There's not a URL, but it seems odd that this would be like this, so let's
            # assume it's mid-edit
            logger.warning(
                "The text on line %d seems to be a link reference definition, but it "
                "does not contain a link. We will be treating it as if it were.",
                index + 1,
            )
            __END_INDEX = index + 1
            return True

        url_and_title = lines[index + 1].split(maxsplit=1)
        if len(url_and_title) == 1:
            # Only the URL is on the next line
            if lines[index + 2].lstrip().startswith("'") or lines[
                index + 2
            ].lstrip().startswith('"'):
                # There's a title starting on the line after that
                rest_of_line = lines[index + 2].lstrip()
                index = index + 2
                url_index = index + 1
            else:
                # There's no title, just the label and URL on separate lines
                __END_INDEX = index + 2
                return True
        else:
            # The title may also be on the next line
            if url_and_title[1].startswith("'") or url_and_title[1].startswith('"'):
                rest_of_line = url_and_title[1]
                index = index + 1
            else:
                # The next line is incorrectly formatted, so we fall back to assuming
                # the link is mid-edit
                logger.warning(
                    "The text on line %d seems to be a link reference definition, but "
                    "it does not contain a link. We will be treating it as if it were.",
                    index + 1,
                )
                __END_INDEX = index + 1
                return True

    if line[match.end() :] == rest_of_line:  # noqa: E203
        raise RuntimeError(
            "`rest_of_line` went unchanged. Please open a bug report or shoot me "
            "an email at jholland@duosecurity.com"
        )

    quotation = rest_of_line[0]
    closing_regex = re.compile(r"(?<!\\)(\\\\)*{}".format(quotation))

    for index, line in enumerate(
        itertools.chain([rest_of_line[1:]], lines[index + 1 :]),
        start=index,  # noqa: E203
    ):
        match = closing_regex.search(line.rstrip())
        if match:
            if match.end() == len(line.rstrip()):
                __END_INDEX = index + 1
                return True
            else:
                if url_index is not None:
                    __END_INDEX = url_index + 1
                    return True
                else:
                    return False

    if url_index is not None:
        __END_INDEX = url_index + 1
        return True
    else:
        return False


def link_reference_definition_ended(line: str, index: int, lines: List[str]) -> bool:
    global __END_INDEX
    if __END_INDEX == index:
        __END_INDEX = -1
        return True
    else:
        return False
