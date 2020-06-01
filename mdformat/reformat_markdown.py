from enum import Enum
import logging

from typing import List
from .typing import Number, SectionEndedFunc

from .detectors import (
    block_quote_started,
    block_quote_ended,
    code_block_started,
    create_code_block_ended_func,
    footnote_started,
    footnote_ended,
    heading_started,
    heading_ended,
    horizontal_line_started,
    horizontal_line_ended,
    list_started,
    list_ended,
    paragraph_started,
    paragraph_ended,
    separator_started,
    separator_ended,
    table_started,
    table_ended,
)
from .exceptions import ReformatInconsistentException
from .formatters import (
    MarkdownBlockQuote,
    MarkdownCodeBlock,
    MarkdownFootnote,
    MarkdownHeading,
    MarkdownHorizontalLine,
    MarkdownList,
    MarkdownParagraph,
    MarkdownSection,
    MarkdownSeparator,
    MarkdownTable,
)

__all__ = ["reformat_markdown_text"]

logger = logging.getLogger(__name__)


class LineState(Enum):
    DEFAULT = "default"
    BLOCK_QUOTE = "block quote"
    CODE_BLOCK = "code block"
    FOOTNOTE = "footnote"
    HEADING = "headings"
    HORIZONTAL_LINE = "horizontal line"
    LIST = "list"
    PARAGRAPH = "paragraph"
    SEPARATOR = "separator"
    TABLE = "table"


def _reformat_markdown_text(text: str, width: Number = 88) -> str:
    """ Reformat a block of markdown text

    See the README for how the Markdown text gets reformatted.

    Args:
        text: The Markdown text to rerender
        width: The maximum line length. Note, for table a code blocks, this length is
            not enforced as the would change the documents appearance when rendered.

    Returns:
        The reformatted Markdown text
    """
    lines = text.splitlines()
    sections: List[MarkdownSection] = []
    state = LineState.DEFAULT
    ended_function: SectionEndedFunc = lambda _line, _i, _lines: False

    for i, line in enumerate(lines):
        if ended_function(line, i, lines):
            state = LineState.DEFAULT

        if state == LineState.DEFAULT:
            if block_quote_started(line, i, lines):
                state = LineState.CODE_BLOCK
                ended_function = block_quote_ended
                sections.append(MarkdownBlockQuote(i))
            elif code_block_started(line, i, lines):
                state = LineState.CODE_BLOCK
                ended_function = create_code_block_ended_func(line, i, lines)
                sections.append(MarkdownCodeBlock(i))
            elif footnote_started(line, i, lines):
                state = LineState.FOOTNOTE
                ended_function = footnote_ended
                sections.append(MarkdownFootnote(i))
            elif heading_started(line, i, lines):
                state = LineState.HEADING
                ended_function = heading_ended
                sections.append(MarkdownHeading(i))
            elif horizontal_line_started(line, i, lines):
                state = LineState.HORIZONTAL_LINE
                ended_function = horizontal_line_ended
                sections.append(MarkdownHorizontalLine(i))
            elif list_started(line, i, lines):
                state = LineState.LIST
                ended_function = list_ended
                sections.append(MarkdownList(i))
            elif paragraph_started(line, i, lines):
                state = LineState.PARAGRAPH
                ended_function = paragraph_ended
                sections.append(MarkdownParagraph(i))
            elif separator_started(line, i, lines):
                state = LineState.SEPARATOR
                ended_function = separator_ended
                sections.append(MarkdownSeparator(i))
            elif table_started(line, i, lines):
                state = LineState.TABLE
                ended_function = table_ended
                sections.append(MarkdownTable(i))
            else:
                raise RuntimeError(f"Could not detect section type on line {i + 1}.")

        sections[-1].append(line)

        logger.debug("Line %d state: %s", i + 1, state)

    if sections and isinstance(sections[-1], MarkdownSeparator):
        sections.pop()

    return "\n".join([section.reformatted(width=width) for section in sections]) + "\n"


def reformat_markdown_text(text: str, width: Number = 88) -> str:
    """ Reformat a block of markdown text

    See the README for how the Markdown text gets reformatted.

    Args:
        text: The Markdown text to rerender
        width: The maximum line length. Note, for table a code blocks, this length is
            not enforced as the would change the documents appearance when rendered.

    Returns:
        The reformatted Markdown text
    """
    new_text = _reformat_markdown_text(text, width)
    if new_text != _reformat_markdown_text(new_text, width):
        raise ReformatInconsistentException(
            f"Reformat of reformatted code results in different text."
        )
    return new_text
