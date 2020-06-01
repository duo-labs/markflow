from typing import List

from .code_block import code_block_started
from .list import list_started


def heading_started(line: str, index: int, lines: List[str]) -> bool:
    if not line.strip():
        return False
    elif line.lstrip().startswith("#") and not code_block_started(line, index, lines):
        return True
    elif list_started(line, index, lines):
        # Lists can't be headings
        return False
    else:
        if len(lines) <= index + 1:
            return False
        lookahead = lines[index + 1]
        if not lookahead.strip():
            return False
        return all([c == "=" for c in lookahead.strip()]) or all(
            [c == "-" for c in lookahead.strip()]
        )


def heading_ended(line: str, index: int, lines: List[str]) -> bool:
    # TODO: Consecutive "---" or "===" lines are errors
    if line.strip() and (
        all([c == "=" for c in line.strip()]) or all([c == "-" for c in line.strip()])
    ):
        return False
    else:
        return True
