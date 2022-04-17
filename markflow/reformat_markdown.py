import logging
from typing import Dict, Type

from .exceptions import ReformatInconsistentException
from .formatters import (
    MarkdownATXHeading,
    MarkdownBlankLine,
    MarkdownBlockQuote,
    MarkdownBulletList,
    MarkdownFencedCodeBlock,
    MarkdownIndentedCodeBlock,
    MarkdownLinkReferenceDefinition,
    MarkdownOrderedList,
    MarkdownParagraph,
    MarkdownSection,
    MarkdownSetextHeading,
    MarkdownTable,
    MarkdownThematicBreak,
)
from .parser import MarkdownSectionEnum, parse_markdown
from .typing import Number

__all__ = ["reformat_markdown_text"]

logger = logging.getLogger(__name__)


FORMATTERS: Dict[MarkdownSectionEnum, Type[MarkdownSection]] = {
    MarkdownSectionEnum.ATX_HEADING: MarkdownATXHeading,
    MarkdownSectionEnum.BLANK_LINE: MarkdownBlankLine,
    MarkdownSectionEnum.BLOCK_QUOTE: MarkdownBlockQuote,
    MarkdownSectionEnum.BULLET_LIST: MarkdownBulletList,
    MarkdownSectionEnum.FENCED_CODE_BLOCK: MarkdownFencedCodeBlock,
    MarkdownSectionEnum.INDENTED_CODE_BLOCK: MarkdownIndentedCodeBlock,
    MarkdownSectionEnum.LINK_REFERENCE_DEFINITION: MarkdownLinkReferenceDefinition,
    MarkdownSectionEnum.ORDERED_LIST: MarkdownOrderedList,
    MarkdownSectionEnum.PARAGRAPH: MarkdownParagraph,
    MarkdownSectionEnum.SETEXT_HEADING: MarkdownSetextHeading,
    MarkdownSectionEnum.TABLE: MarkdownTable,
    MarkdownSectionEnum.THEMATIC_BREAK: MarkdownThematicBreak,
}


def _reformat_markdown_text(text: str, width: Number = 88, line_index: int = 0) -> str:
    sections = parse_markdown(text.splitlines())

    formatters = []
    last_section_type = MarkdownSectionEnum.INVALID

    for section_type, section_content in sections:
        formatter = FORMATTERS[section_type](line_index, section_content)
        content_length = len(section_content)
        if content_length > 1:
            log_text = f"Lines {line_index + 1}-{line_index + content_length}"
        else:
            log_text = f"Line {line_index + 1}"
        logger.info("%s: %s", log_text, repr(formatter))
        if (
            section_type == MarkdownSectionEnum.SETEXT_HEADING
            and last_section_type == MarkdownSectionEnum.BLOCK_QUOTE
        ):
            logger.warning(
                f"Adding a new line before setext heading on line {line_index + 1}"
            )
            formatters.append(
                FORMATTERS[MarkdownSectionEnum.BLANK_LINE](line_index, [""])
            )
        formatters.append(formatter)
        line_index += len(section_content)

        last_section_type = section_type

    return "\n".join(f.reformatted(width) for f in formatters) + "\n"


def reformat_markdown_text(text: str, width: Number = 88) -> str:
    """Reformat a block of markdown text

    See the README for how the Markdown text gets reformatted.

    Args:
        text: The Markdown text toblo rerender
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
            "Reformat of reformatted code results in different text. Please open a bug "
            "report or email jholland@duosecurity.com."
        )
    new_text = new_text.rstrip() + "\n"
    return new_text
