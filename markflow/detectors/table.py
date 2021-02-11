from typing import List, Tuple


def table_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return line.lstrip().startswith("|")


def table_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    return not table_started(line, index, lines)


def split_table(lines: List[str], line_offset: int = 0) -> Tuple[List[str], List[str]]:
    table = []
    remaining_lines = lines

    index = 0
    if table_started(lines[index], index, lines):
        table.append(lines[index])
        for index, line in enumerate(lines[1:], start=index + 1):
            if table_ended(line, index, lines):
                break
            table.append(line)
        else:
            index += 1
    remaining_lines = lines[index:]

    return table, remaining_lines
