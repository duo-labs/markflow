import functools

from typing import cast, List
from ..typing import SectionEndedFunc


def code_block_started(line: str, index: int, lines: List[str]) -> bool:
    return tilda_code_block_started(line, index, lines) or indented_code_block_started(
        line, index, lines
    )


def tilda_code_block_started(line: str, index: int, lines: List[str]) -> bool:
    return line.strip().startswith("``")


def indented_code_block_started(line: str, index: int, lines: List[str]) -> bool:
    return bool(line.strip()) and line.startswith("    ")


def _tilda_code_block_ended(
    line: str, index: int, lines: List[str], initial_index: int, ending: str = "``"
) -> bool:
    if index == initial_index + 1:
        return False
    else:
        return lines[index - 1].strip().startswith(ending)


def _indented_code_block_ended(line: str, index: int, lines: List[str]) -> bool:
    if not line.strip():
        # If we find a blank line, we need to check and see if the next non-blank line
        # is not indented
        for line in lines[index:]:
            # We've found a blank line
            if not line.strip():
                continue
            if line.startswith("    "):
                return False
            else:
                return True
        else:
            return False
    elif line.startswith("    "):
        return False
    else:
        return True


def create_code_block_ended_func(
    line: str, index: int, lines: List[str]
) -> SectionEndedFunc:
    if line.startswith("    "):
        return _indented_code_block_ended
    tilda_count = 0
    for c in line.lstrip():
        if c == "`":
            tilda_count += 1
        else:
            break
    ending = "`" * tilda_count

    return cast(
        SectionEndedFunc,
        functools.partial(_tilda_code_block_ended, initial_index=index, ending=ending),
    )
