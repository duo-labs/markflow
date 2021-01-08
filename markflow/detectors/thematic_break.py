from typing import List

from .code_block import indented_code_block_started

SEPARATOR_SYMBOLS = ["*", "_", "-"]


def thematic_break_started(line: str, index: int, lines: List[str]) -> bool:
    if indented_code_block_started(line, index, lines):
        return False
    elif len(line.strip()) < 3:
        # Thematic breaks must be at least three characters long
        return False
    else:
        for symbol in SEPARATOR_SYMBOLS:
            if all(char == symbol for char in line.strip()):
                return True
        return False


def thematic_break_ended(line: str, index: int, lines: List[str]) -> bool:
    return True
