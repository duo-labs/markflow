import logging
from enum import Enum
from typing import List, Tuple

from .detectors import (
    split_atx_heading,
    split_blank_line,
    split_block_quote,
    split_bullet_list,
    split_fenced_code_block,
    split_indented_code_block,
    split_link_reference_definition,
    split_ordered_list,
    split_paragraph,
    split_setext_heading,
    split_table,
    split_thematic_break,
)
from .typing import SplitFunc

logger = logging.getLogger(__name__)


class MarkdownSectionEnum(Enum):
    INVALID = "Invalid"
    ATX_HEADING = "ATX Heading"
    BLANK_LINE = "Blank Line"
    BLOCK_QUOTE = "Block Quote"
    BULLET_LIST = "Bullet List"
    FENCED_CODE_BLOCK = "Fenced Code Block"
    INDENTED_CODE_BLOCK = "Indented Code Block"
    LINK_REFERENCE_DEFINITION = "Link Reference Definition"
    ORDERED_LIST = "Ordered List"
    PARAGRAPH = "Paragraph"
    SETEXT_HEADING = "Setext Heading"
    TABLE = "Table"
    THEMATIC_BREAK = "Thematic Break"


SPLITTERS: List[Tuple[MarkdownSectionEnum, SplitFunc]] = [
    (MarkdownSectionEnum.ATX_HEADING, split_atx_heading),
    (MarkdownSectionEnum.BLANK_LINE, split_blank_line),
    (MarkdownSectionEnum.BLOCK_QUOTE, split_block_quote),
    (MarkdownSectionEnum.BULLET_LIST, split_bullet_list),
    (MarkdownSectionEnum.FENCED_CODE_BLOCK, split_fenced_code_block),
    (MarkdownSectionEnum.INDENTED_CODE_BLOCK, split_indented_code_block),
    (MarkdownSectionEnum.LINK_REFERENCE_DEFINITION, split_link_reference_definition),
    (MarkdownSectionEnum.ORDERED_LIST, split_ordered_list),
    (MarkdownSectionEnum.PARAGRAPH, split_paragraph),
    (MarkdownSectionEnum.SETEXT_HEADING, split_setext_heading),
    (MarkdownSectionEnum.TABLE, split_table),
    (MarkdownSectionEnum.THEMATIC_BREAK, split_thematic_break),
]


def parse_markdown(lines: List[str]) -> List[Tuple[MarkdownSectionEnum, List[str]]]:
    sections: List[Tuple[MarkdownSectionEnum, List[str]]] = []
    remaining_lines = lines
    current_line = 1

    while remaining_lines:
        for section_type, splitter in SPLITTERS:
            section_content, remaining_lines = splitter(remaining_lines)
            if section_content:
                content_length = len(section_content)
                if content_length > 1:
                    log_text = (
                        f"Lines {current_line}-{current_line + content_length - 1}"
                    )
                else:
                    log_text = f"Line {current_line}"
                logger.debug(
                    "%s: %s", log_text, section_type.value,
                )
                sections.append((section_type, section_content))
                current_line += len(section_content)
                break
        else:
            raise RuntimeError(
                f"Could not determine section type on line {current_line}",
            )

    return sections
