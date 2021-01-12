from typing import List, Tuple

from .list import list_started
from .blank_line import blank_line_started
from .._utils import get_indent


def block_quote_started(line: str, index: int, lines: List[str]) -> bool:
    if get_indent(line) >= 4:
        return False

    return line.lstrip().startswith(">")


def block_quote_ended(line: str, index: int, lines: List[str]) -> bool:
    return blank_line_started(line, index, lines) or list_started(line, index, lines)


def split_block_quote(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    block_quote = []
    remaining_lines = lines

    index = 0
    if block_quote_started(lines[index], index, lines):
        block_quote.append(lines[index])
        for index, line in enumerate(lines[1:], start=index + 1):
            if block_quote_ended(line, index, lines):
                break
            block_quote.append(line)
        else:
            index += 1
    remaining_lines = lines[index:]

    return block_quote, remaining_lines
