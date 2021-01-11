from enum import Enum
import logging

from typing import List
from .typing import Number, SectionEndedFunc

from .detectors import (
    atx_heading_started,
    atx_heading_ended,
    blank_line_started,
    blank_line_ended,
    block_quote_started,
    block_quote_ended,
    fenced_code_block_started,
    fenced_code_block_ended,
    indented_code_block_started,
    indented_code_block_ended,
    link_reference_definition_started,
    link_reference_definition_ended,
    list_started,
    list_ended,
    paragraph_started,
    paragraph_ended,
    setext_heading_started,
    setext_heading_ended,
    table_started,
    table_ended,
    thematic_break_started,
    thematic_break_ended,
)
from .exceptions import ReformatInconsistentException
from .formatters import (
    MarkdownATXHeading,
    MarkdownBlockQuote,
    MarkdownFencedCodeBlock,
    MarkdownIndentedCodeBlock,
    MarkdownLinkReferenceDefinition,
    MarkdownList,
    MarkdownParagraph,
    MarkdownSection,
    MarkdownBlankLine,
    MarkdownSetextHeading,
    MarkdownTable,
    MarkdownThematicBreak,
)

__all__ = ["reformat_markdown_text"]

logger = logging.getLogger(__name__)


class LineState(Enum):
    DEFAULT = "default"
    ATX_HEADING = "atx heading"
    BLANK_LINE = "blank line"
    BLOCK_QUOTE = "block quote"
    CODE_BLOCK = "code block"
    FENCED_CODE_BLOCK = "fence code block"
    HEADING = "headings"
    INDENTED_CODE_BLOCK = "indented code block"
    LINK_REFERENCE_DEFINITION = "link reference definition"
    LIST = "list"
    PARAGRAPH = "paragraph"
    SETEXT_HEADING = "setext heading"
    TABLE = "table"
    THEMATIC_BREAK = "thematic break"


def _reformat_markdown_text(
    text: str, width: Number = 88, log_sections: bool = True
) -> str:
    """Reformat a block of markdown text

    See the README for how the Markdown text gets reformatted.

    Args:
        text: The Markdown text to rerender
        width: The maximum line length. Note, for table a code blocks, this length is
            not enforced as the would change the documents appearance when rendered.
        log_sections: Whether or not sections should be logged. Useful for shutting down
            logging during second passes. I wonder if this would be done better by
            configuring a specific logger. (ToDo)

    Returns:
        The reformatted Markdown text
    """
    lines = text.splitlines()
    sections: List[MarkdownSection] = []
    state = LineState.DEFAULT
    ended_function: SectionEndedFunc = lambda _line, _i, _lines: False
    start = -1

    for index, line in enumerate(lines):
        if ended_function(line, index, lines):
            state = LineState.DEFAULT

        if state == LineState.DEFAULT:
            if sections and log_sections:
                if start + 1 == index:
                    words = f"Line {start + 1}"
                else:
                    words = f"Lines {start + 1}-{index}"
                logger.info("%s: %s", words, repr(sections[-1]))
            start = index

            if atx_heading_started(line, index, lines):
                state = LineState.ATX_HEADING
                ended_function = atx_heading_ended
                sections.append(MarkdownATXHeading(index))
            elif blank_line_started(line, index, lines):
                state = LineState.BLANK_LINE
                ended_function = blank_line_ended
                sections.append(MarkdownBlankLine(index))
            elif block_quote_started(line, index, lines):
                state = LineState.CODE_BLOCK
                ended_function = block_quote_ended
                sections.append(MarkdownBlockQuote(index))
            elif indented_code_block_started(line, index, lines):
                state = LineState.INDENTED_CODE_BLOCK
                ended_function = indented_code_block_ended
                sections.append(MarkdownIndentedCodeBlock(index))
            elif fenced_code_block_started(line, index, lines):
                state = LineState.FENCED_CODE_BLOCK
                ended_function = fenced_code_block_ended
                sections.append(MarkdownFencedCodeBlock(index))
            elif link_reference_definition_started(line, index, lines):
                state = LineState.LINK_REFERENCE_DEFINITION
                ended_function = link_reference_definition_ended
                sections.append(MarkdownLinkReferenceDefinition(index))
            elif list_started(line, index, lines):
                state = LineState.LIST
                ended_function = list_ended
                sections.append(MarkdownList(index))
            # This must be checked before paragraph checking.
            elif setext_heading_started(line, index, lines):
                state = LineState.SETEXT_HEADING
                ended_function = setext_heading_ended
                sections.append(MarkdownSetextHeading(index))
            elif paragraph_started(line, index, lines):
                state = LineState.PARAGRAPH
                ended_function = paragraph_ended
                sections.append(MarkdownParagraph(index))
            elif table_started(line, index, lines):
                state = LineState.TABLE
                ended_function = table_ended
                sections.append(MarkdownTable(index))
            elif thematic_break_started(line, index, lines):
                state = LineState.THEMATIC_BREAK
                ended_function = thematic_break_ended
                sections.append(MarkdownThematicBreak(index))
            else:
                raise RuntimeError(
                    f"Could not detect section type on line {index + 1}."
                )

        sections[-1].append(line)

        logger.debug("Line %d state: %s", index + 1, state)

    if sections and log_sections:
        if start == index:
            words = f"Line {start + 1}"
        else:
            words = f"Lines {start + 1}-{index}"
        logger.info("%s: %s", words, repr(sections[-1]))

    if sections and isinstance(sections[-1], MarkdownBlankLine):
        sections.pop()

    while sections and isinstance(sections[0], MarkdownBlankLine):
        sections.pop(0)
    while sections and isinstance(sections[-1], MarkdownBlankLine):
        sections.pop(-1)

    return "\n".join([section.reformatted(width=width) for section in sections]) + "\n"


def reformat_markdown_text(text: str, width: Number = 88) -> str:
    """Reformat a block of markdown text

    See the README for how the Markdown text gets reformatted.

    Args:
        text: The Markdown text to rerender
        width: The maximum line length. Note, for table a code blocks, this length is
            not enforced as the would change the documents appearance when rendered.

    Returns:
        The reformatted Markdown text
    """
    new_text = _reformat_markdown_text(text, width)
    level = logger.getEffectiveLevel()
    # Mute logging during second pass since it means nothing to the user.
    if level > logging.DEBUG:
        logger.setLevel(logging.ERROR)
    new_new_text = _reformat_markdown_text(new_text, width)
    logger.setLevel(level)
    if new_new_text != new_text:
        raise ReformatInconsistentException(
            f"Reformat of reformatted code results in different text. Please open a "
            f"bug report or email jholland@duosecurity.com."
        )

    return new_text
