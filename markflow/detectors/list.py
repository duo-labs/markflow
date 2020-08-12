import re

from typing import List

from .horizontal_line import horizontal_line_started
from .separator import separator_started
from .table import table_started


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
        horizontal_line_started(line, index, lines)
        or table_started(line, index, lines)
        or separator_started(line, index, lines)
    )
