"""
MarkFlow Link Reference Definition Detection Library

Link reference definitions are intended to be unrendered portions of a document that
provide a short hand for links. The start with a series of non-whitespace characters
enclosed in brackets ([]) that serve as the label. It is followed by a colon (:) and
optional whitespace. That is then followed by a series of non-whitespace characters that
serve as the link. This can optionally be followed by white-space and then a quotation
(' or ") enclosed series of characters that serves as the title. Any of the optional
whitespace may be a new line.

Examples:
    ```
    [label]: link 'title'

    [label]: link
    'title'

    [label]:
    link
    'title'
    ```
"""

import itertools
import logging
import re
from typing import List, Tuple

from .._utils import get_indent

logger = logging.getLogger(__name__)

LINK_REFERENCE_DEFINITION_FIRST_ELEMENT_REGEX = re.compile(
    r"\["  # Open bracket
    r"[^\]]{1,999}"  # At least one and up to 999 characters as the name
    r"\]:"  # End bracket and colon
)
QUOTATION_CHARACTERS = "'\""


def split_link_reference_definition(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split leading link reference definition from lines if one exists

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the indented code block lines if they were
        found, otherwise it is an empty list. The second value is the remaining text.
        (If lines does not start with a link reference definition, it is the same as
        lines.)
    """
    link_reference_definition: List[str] = []
    remaining_lines = lines
    indexed_line_generator = enumerate(lines)

    index, line = next(indexed_line_generator)

    if get_indent(line) >= 4:
        return link_reference_definition, remaining_lines

    rest_of_line = line.lstrip()
    match = LINK_REFERENCE_DEFINITION_FIRST_ELEMENT_REGEX.match(rest_of_line)
    if not match:
        return link_reference_definition, remaining_lines

    rest_of_line = rest_of_line[match.end() :]
    url_and_title = rest_of_line.split(maxsplit=1)
    # At the end of this, index is set to the line with the beginning of the title_text
    # contains that first text. Is complete gets set from this loop when we know that
    # we have a valid title. In this first loop, we only set it when we know the lines
    # with the label and URL can stand on their own.
    # The later loops checks to ensure our closing quotation is the last non-whitespace
    # character on whatever line it ends on and the first occurence of that character,
    # unescaped.
    is_complete = False
    if len(url_and_title) == 2:
        # The label, URL, and possible title (or part of it) are on this line
        title_text = url_and_title[1]
    elif len(url_and_title) == 1:
        # Only the label and URL are on the first line
        try:
            index, line = next(indexed_line_generator)
            title_text = line
        except StopIteration:
            title_text = ""
        is_complete = True
    else:
        # Just the label was on the first line
        try:
            index, line = next(indexed_line_generator)
        except StopIteration:
            line = ""
        if line.startswith("[") or not line.strip():
            # According to this standard, this is just paragraph text, but this tool
            # should be usable during development.
            # ToDo: Does that match up with our treatment of misquoted titles?
            logger.warning(
                "The text on line %d seems to be a link reference definition, but it "
                "does not contain a link. We will be treating it as if it were.",
                index,  # We are just pass where the issue exists
            )
            link_reference_definition = [lines[0]]
            remaining_lines = lines[1:]
            return link_reference_definition, remaining_lines
        elif len(line.split(maxsplit=1)) == 1:
            # Only the URL is on the second line
            index, line = next(indexed_line_generator)
            is_complete = True
            title_text = line
        else:
            # The URL and possible title (or part of it) are on the second line
            title_text = line.split(maxsplit=1)[1]

    if title_text.strip():
        quotation_character = title_text[0]
    else:
        quotation_character = "NO QUOTE"

    if quotation_character in QUOTATION_CHARACTERS:
        closing_regex = re.compile(r"(?<!\\)(\\\\)*{}".format(quotation_character))
        for index, line in itertools.chain(
            [(index, title_text[1:])], indexed_line_generator
        ):
            match = closing_regex.search(line.rstrip())
            if match:
                if match.end() == len(line.rstrip()):
                    is_complete = True
                    index += 1
                break

    if is_complete:
        link_reference_definition = lines[:index]
        remaining_lines = lines[index:]

    return link_reference_definition, remaining_lines
