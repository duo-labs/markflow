from typing import List, Tuple

from ._lines import is_blank_line_line, is_block_quote_line, is_list_start_line


def block_quote_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return is_block_quote_line(line)


def block_quote_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return is_blank_line_line(line) or is_list_start_line(line)


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
