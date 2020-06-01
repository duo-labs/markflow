from typing import List


def table_started(line: str, index: int, lines: List[str]) -> bool:
    return line.lstrip().startswith("|")


def table_ended(line: str, index: int, lines: List[str]) -> bool:
    return not table_started(line, index, lines)
