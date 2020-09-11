from typing import List

from .code_block import indented_code_block_started

SEPARATOR_SYMBOLS = ["*", "_", "-"]


def horizontal_line_started(line: str, index: int, lines: List[str]) -> bool:
    if indented_code_block_started(line, index, lines):
        return False
    elif len(line.strip()) < 3:
        # Horizontal lines must be at least three characters long
        return False
    else:
        for symbol in SEPARATOR_SYMBOLS:
            if all(char == symbol for char in line.strip()):
                return True
        return False


def horizontal_line_ended(line: str, index: int, lines: List[str]) -> bool:
    return True
