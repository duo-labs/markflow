from typing import List

from .code_block import indented_code_block_started


def horizontal_line_started(line: str, index: int, lines: List[str]) -> bool:
    return (
        not indented_code_block_started(line, index, lines)
        and len(line.strip()) >= 3
        and all(c == "-" for c in line.strip())
    )


def horizontal_line_ended(line: str, index: int, lines: List[str]) -> bool:
    return True
