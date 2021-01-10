from enum import Enum
import logging

from typing import List
from .typing import Number, SectionEndedFunc

from .detectors import (
    atx_heading_started,
    atx_heading_ended,
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
    separator_started,
    separator_ended,
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
    MarkdownSeparator,
    MarkdownSetextHeading,
    MarkdownTable,
    MarkdownThematicBreak,
)

__all__ = ["reformat_markdown_text"]

logger = logging.getLogger(__name__)


class LineState(Enum):
    DEFAULT = "default"
    ATX_HEADING = "atx heading"
    BLOCK_QUOTE = "block quote"
    CODE_BLOCK = "code block"
    FENCED_CODE_BLOCK = "fence code block"
    HEADING = "headings"
    INDENTED_CODE_BLOCK = "indented code block"
    LINK_REFERENCE_DEFINITION = "link reference definition"
    LIST = "list"
    PARAGRAPH = "paragraph"
    SEPARATOR = "separator"
    SETEXT_HEADING = "setext heading"
    TABLE = "table"
    THEMATIC_BREAK = "thematic break"


def _reformat_markdown_text(text: str, width: Number = 88) -> str:
    """Reformat a block of markdown text

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
            if sections:
                logger.info("Last section: %s", repr(sections[-1]))

            if atx_heading_started(line, i, lines):
                state = LineState.ATX_HEADING
                ended_function = atx_heading_ended
                sections.append(MarkdownATXHeading(i))
            elif block_quote_started(line, i, lines):
                state = LineState.CODE_BLOCK
                ended_function = block_quote_ended
                sections.append(MarkdownBlockQuote(i))
            elif indented_code_block_started(line, i, lines):
                state = LineState.INDENTED_CODE_BLOCK
                ended_function = indented_code_block_ended
                sections.append(MarkdownIndentedCodeBlock(i))
            elif fenced_code_block_started(line, i, lines):
                state = LineState.FENCED_CODE_BLOCK
                ended_function = fenced_code_block_ended
                sections.append(MarkdownFencedCodeBlock(i))
            elif link_reference_definition_started(line, i, lines):
                state = LineState.LINK_REFERENCE_DEFINITION
                ended_function = link_reference_definition_ended
                sections.append(MarkdownLinkReferenceDefinition(i))
            elif list_started(line, i, lines):
                state = LineState.LIST
                ended_function = list_ended
                sections.append(MarkdownList(i))
            # This must be checked before paragraph checking.
            elif setext_heading_started(line, i, lines):
                state = LineState.SETEXT_HEADING
                ended_function = setext_heading_ended
                sections.append(MarkdownSetextHeading(i))
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
            elif thematic_break_started(line, i, lines):
                state = LineState.THEMATIC_BREAK
                ended_function = thematic_break_ended
                sections.append(MarkdownThematicBreak(i))
            else:
                raise RuntimeError(f"Could not detect section type on line {i + 1}.")

        sections[-1].append(line)

        logger.debug("Line %d state: %s", i + 1, state)

    if sections:
        logger.info("Last section: %s", repr(sections[-1]))

    if sections and isinstance(sections[-1], MarkdownSeparator):
        sections.pop()

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
    if new_text != _reformat_markdown_text(new_text, width):
        raise ReformatInconsistentException(
            f"Reformat of reformatted code results in different text."
        )
    return new_text
