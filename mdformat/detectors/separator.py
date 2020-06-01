from typing import List


def separator_started(line: str, index: int, lines: List[str]) -> bool:
    return not line.strip()


def separator_ended(line: str, index: int, lines: List[str]) -> bool:
    return not separator_started(line, index, lines)
