from typing import List

from .block_quote import block_quote_started
from .code_block import code_block_started, tilda_code_block_started
from .heading import heading_started
from .horizontal_line import horizontal_line_started
from .list import list_started
from .separator import separator_started
from .table import table_started


def paragraph_started(line: str, index: int, lines: List[str]) -> bool:
    return not (
        block_quote_started(line, index, lines)
        or code_block_started(line, index, lines)
        or heading_started(line, index, lines)
        or horizontal_line_started(line, index, lines)
        or list_started(line, index, lines)
        or separator_started(line, index, lines)
        or table_started(line, index, lines)
    )


def paragraph_ended(line: str, index: int, lines: List[str]) -> bool:
    return (
        block_quote_started(line, index, lines)
        or tilda_code_block_started(line, index, lines)
        or heading_started(line, index, lines)
        or horizontal_line_started(line, index, lines)
        or list_started(line, index, lines)
        or separator_started(line, index, lines)
    )
