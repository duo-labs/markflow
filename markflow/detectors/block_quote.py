from typing import List

from .indented_code_block import indented_code_block_started
from .list import list_started
from .blank_line import blank_line_started


def block_quote_started(line: str, index: int, lines: List[str]) -> bool:
    return not indented_code_block_started(
        line, index, lines
    ) and line.lstrip().startswith(">")


def block_quote_ended(line: str, index: int, lines: List[str]) -> bool:
    return blank_line_started(line, index, lines) or list_started(line, index, lines)
