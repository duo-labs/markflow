from typing import List

from .atx_heading import atx_heading_started
from .block_quote import block_quote_started
from .code_block import code_block_started, tilda_code_block_started
from .list import list_started
from .separator import separator_started
from .table import table_started
from .thematic_break import thematic_break_started


def paragraph_started(line: str, index: int, lines: List[str]) -> bool:
    return not (
        atx_heading_started(line, index, lines)
        or block_quote_started(line, index, lines)
        or code_block_started(line, index, lines)
        or list_started(line, index, lines)
        or separator_started(line, index, lines)
        # A setext heading is just a paragraph with a line of - or = after
        or table_started(line, index, lines)
        or thematic_break_started(line, index, lines)
    )


def paragraph_ended(line: str, index: int, lines: List[str]) -> bool:
    return (
        ((index > 0) and lines[index - 1].endswith("  "))
        or atx_heading_started(line, index, lines)
        or block_quote_started(line, index, lines)
        or tilda_code_block_started(line, index, lines)
        or list_started(line, index, lines)
        or separator_started(line, index, lines)
        # A setext heading cannot interrupt a paragraph (CommonMark 0.29 4.3)
        or thematic_break_started(line, index, lines)
    )
