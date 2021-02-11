from typing import List, Tuple

from ._lines import (
    is_blank_line_line,
    is_list_start_line,
    is_table_start_line,
    is_thematic_break_line,
)


def list_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return is_list_start_line(line)


def list_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return (
        is_blank_line_line(line)
        or is_table_start_line(line)
        or is_thematic_break_line(line)
    )


def split_list(lines: List[str], line_offset: int = 0) -> Tuple[List[str], List[str]]:
    list_ = []
    remaining_lines = lines

    index = 0
    if list_started(lines[index], index, lines):
        list_.append(lines[index])
        for index, line in enumerate(lines[1:], start=index + 1):
            if list_ended(line, index, lines):
                break
            list_.append(line)
        else:
            index += 1
    remaining_lines = lines[index:]

    return list_, remaining_lines
