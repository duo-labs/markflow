from typing import List, Tuple

from .atx_heading import atx_heading_started
from .blank_line import blank_line_started
from .block_quote import block_quote_started
from .fenced_code_block import fenced_code_block_started
from .list import list_started
from .table import table_started
from .thematic_break import thematic_break_started
from .._utils import get_indent


def paragraph_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    if get_indent(line) >= 4:
        return False

    return not (
        atx_heading_started(line, index, lines)
        or blank_line_started(line, index, lines)
        or block_quote_started(line, index, lines)
        or fenced_code_block_started(line, index, lines)
        or list_started(line, index, lines)
        # A setext heading is just a paragraph with a line of - or = after
        or table_started(line, index, lines)
        or thematic_break_started(line, index, lines)
    )


def paragraph_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return (
        ((index > 0) and lines[index - 1].endswith("  "))
        or atx_heading_started(line, index, lines)
        or block_quote_started(line, index, lines)
        or fenced_code_block_started(line, index, lines)
        or list_started(line, index, lines)
        or blank_line_started(line, index, lines)
        # A setext heading cannot interrupt a paragraph (CommonMark 0.29 4.3)
        # ToDo: setext and paragraphs should call a common function and switch on this.
        or thematic_break_started(line, index, lines)
    )


def split_paragraph(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    paragraph = []
    remaining_lines = lines

    index = 0
    if paragraph_started(lines[index], index, lines):
        paragraph.append(lines[index])
        index = index + 1
        for index, line in enumerate(lines[1:], start=index):
            if paragraph_ended(line, index, lines):
                break
            paragraph.append(line)
        else:
            index += 1
    remaining_lines = lines[index:]

    return paragraph, remaining_lines
