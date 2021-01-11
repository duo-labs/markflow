from typing import List

from .list import list_started
from .blank_line import blank_line_started
from .._utils import line_is_indented_at_least


def block_quote_started(line: str, index: int, lines: List[str]) -> bool:
    if line_is_indented_at_least(line, 4):
        return False

    return line.lstrip().startswith(">")


def block_quote_ended(line: str, index: int, lines: List[str]) -> bool:
    return blank_line_started(line, index, lines) or list_started(line, index, lines)
