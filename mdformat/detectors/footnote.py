import re

from typing import List


FOOTNOTE_REGEX = re.compile(r"\s*\[[^\]]+\]\s*:")


def footnote_started(line: str, index: int, lines: List[str]) -> bool:
    return bool(FOOTNOTE_REGEX.search(line))


def footnote_ended(line: str, index: int, lines: List[str]) -> bool:
    return not footnote_started(line, index, lines)
