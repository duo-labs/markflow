import re

from typing import List

from .blank_line import blank_line_started
from .table import table_started
from .thematic_break import thematic_break_started


LIST_REGEX = re.compile(
    r"^\s*"  # Leading spaces are OK and often expected
    r"("
    r"\*|"  # Asterisk list marker
    r"-|"  # Dash list marker
    r"[0-9]+\."  # Numeric list marker
    r") "  # Lists need a space after their identifier
)


def list_started(line: str, index: int, lines: List[str]) -> bool:
    return bool(LIST_REGEX.search(line))


def list_ended(line: str, index: int, lines: List[str]) -> bool:
    return (
        blank_line_started(line, index, lines)
        or table_started(line, index, lines)
        or thematic_break_started(line, index, lines)
    )
